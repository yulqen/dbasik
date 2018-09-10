import csv
import logging
import re
from collections import OrderedDict
from typing import List

from django.contrib import messages
from django.db import IntegrityError
from django.forms import Form
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from register.models import Tier
from .forms import (
    UploadDatamap,
    DatamapForm,
    DatamapLineForm,
    DatamapLineEditForm,
    CSVForm,
)
from .models import Datamap, DatamapLine

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# datamap view functions


class DatamapDelete(DeleteView):
    model = Datamap
    success_url = reverse_lazy("datamaps:datamap_list")


class DatamapUpdate(UpdateView):
    model = Datamap
    template_name_suffix = "_update"
    form_class = DatamapForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Datamap.objects.all()
        context["existing_objects"] = existing_objects
        return context


class DatamapCreate(CreateView):
    model = Datamap
    template_name_suffix = "_create"
    form_class = DatamapForm

    def get_success_url(self, **kwargs):
        name_field = self.request.POST["name"]
        tier_id = self.request.POST["tier"]
        tier_name = get_object_or_404(Tier, pk=tier_id).name
        slugged = slugify("-".join([name_field, tier_name]))
        return reverse_lazy("datamaps:uploaddatamap", args=[slugged])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Datamap.objects.all()
        context["existing_objects"] = existing_objects
        return context


def datamap_detail(request, slug):
    dm_lines = DatamapLine.objects.filter(datamap__slug=slug).order_by("id")
    dms = Datamap.objects.all()
    dm_name = Datamap.objects.get(slug=slug).name
    dm = get_object_or_404(Datamap, slug=slug)
    context = {"dms": dms, "dm_lines": dm_lines, "dm_name": dm_name, "dm": dm}
    return render(request, "datamap/datamap_detail.html", context)


class DatamapList(ListView):
    model = Datamap


class DatamapLineCreate(CreateView):

    model = DatamapLine
    form_class = DatamapLineForm

    def get_form_kwargs(self):
        kargs = super().get_form_kwargs()
        kargs["datamap_id"] = Datamap.objects.get(slug=self.kwargs["slug"]).id
        return kargs

    def get_success_url(self):
        return reverse("datamaps:datamap_detail", args=[self.kwargs["slug"]])


class DatamapLineUpdate(UpdateView):
    model = DatamapLine
    form_class = DatamapLineEditForm

    def get_success_url(self):
        dm_slug = get_object_or_404(DatamapLine, pk=self.kwargs["pk"]).datamap.slug
        #       return reverse("datamaps:datamapline_detail", kwargs={'pk': self.object.pk})
        return reverse("datamaps:datamap_detail", kwargs={"slug": dm_slug})


class DatamapLineDelete(DeleteView):
    model = DatamapLine

    def get_success_url(self):
        dm_slug = get_object_or_404(DatamapLine, pk=self.kwargs["pk"]).datamap.slug
        return reverse("datamaps:datamap_detail", kwargs={"slug": dm_slug})


def _process(row, dm_instance):
    """Save datamap line to database.
    """
    dml = DatamapLine(
        datamap=dm_instance,
        key=row["key"],
        sheet=row["sheet"],
        cell_ref=row["cell_ref"],
    )
    logger.debug(f"Saving {dml.key} | {dml.sheet} | {dml.cell_ref} to database")
    dml.save()


def _remove_dmlines_for_dm(dm_instance: Datamap):
    """Remove all datamapline objects for a particular datamap"""
    DatamapLine.objects.filter(datamap=dm_instance).delete()
    logger.info(f"Removed all datamaplines for {dm_instance}")


def _parse_integrity_exception(errors: List):
    """Take a list of errors and parse the useful messages out"""
    regex = re.compile(r"=\(\d+, (.+), ([A-Z]+\d+)\)")
    temp_list = [x.args[0].split("\n")[1] for x in errors]
    message_list = []
    for i in temp_list:
        m = re.search(regex, i)
        if m:
            mess = " -> ".join([m.group(1), m.group(2)])
            message_list.append(
                f"Duplicate key: {mess} - you can't have that in a datamap!"
            )
    return message_list


def _add_integrity_errors_to_messages(
    request, datamap_obj: Datamap, message_list: List
):
    _remove_dmlines_for_dm(datamap_obj)
    mess = _parse_integrity_exception(message_list)
    for m in mess:
        messages.add_message(request, messages.ERROR, m)


# noinspection Pylint
class UploadDatamapView(FormView):
    template_name = "datamap/upload_datamap.html"
    form_class = UploadDatamap

    def get_success_url(self):
        return reverse_lazy("datamaps:datamap_detail", args=[self.kwargs["slug"]])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.datamap: Datamap = None
        self.errors: list = []
        self._tmp_registered_dml_ids: list = []
        self._existing_dmls_cache: list = []

    def post(self, request, *args, **kwargs):
        form: Form = self.get_form()
        self.datamap = Datamap.objects.get(slug=kwargs["slug"])
        if form.is_valid():
            return self.process_csv(request, form)
        else:
            self._send_errors_to_messages(request, form)
            return self.form_invalid(form)

    def process_csv(self, request, main_form: Form) -> HttpResponseRedirect:
        """
        Processes the CSV form sent in by the form on the Upload Datamap
        page. If not exceptions are thrown, the main_form object passed
        in is used to return valid or invalid to the FormView.

        If a line in the CSV form is not valid, ValueError is thrown
        from this method and form_invalid is returned to FormView and
        a message is passed to the template.

        If a line in the CSV form results in an IntegrityError, because
        there is an existing identical line in the database, this method
        throws the IntegrityError and returns form_invalid to FormView
        and a message is passed to the template.

        Will attempt to roll back the DatamapLine table upon exception.

        :param request:
        :type request: django.core.handlers.wsgi.WSGIRequest
        :param main_form:
        :type main_form: datamap.forms.UploadDatamap
        :return: django.http.response.HttpResponseRedirect
        :rtype: django.http.response.HttpResponseRedirect
        """
        uploaded_file_data = request.FILES["uploaded_file"].readlines()
        reader = csv.DictReader(x.decode("utf-8") for x in uploaded_file_data)
        _timeround = 0
        for line in reader:
            csv_form = CSVForm(line)
            if csv_form.is_valid():
                try:
                    self._create_new_dml_with_line_from_csv(_timeround, line)
                except IntegrityError:
                    self._add_database_error_to_messages(request, line)
                    return self.form_valid(main_form)
                except ValueError:
                    self._send_errors_to_messages(request, csv_form)
                    return self.form_valid(main_form)
            else:
                self._send_errors_to_messages(request, csv_form)
                return self.form_valid(main_form)
            _timeround += 1
        return self.form_valid(main_form)

    def _add_database_error_to_messages(self, request, line: OrderedDict) -> None:
        """
        Constructs a message to be used by the view template based on a single
        OrderedDict, line.
        :param request:
        :type request: django.core.handlers.wsgi.WSGIRequest
        :param line:
        :type line: collections.OrderedDict
        :return:
        :rtype: None
        """
        err_str = self._parse_kwargs_to_error_string(line)
        messages.add_message(request, messages.ERROR, err_str)
        [
            DatamapLine.objects.get(id=dm_id).delete()
            for dm_id in self._tmp_registered_dml_ids
        ]
        for x in self._existing_dmls_cache:
            x.save()
        self._tmp_registered_dml_ids = []
        self._existing_dmls_cache = []

    def _create_new_dml_with_line_from_csv(
        self, _timeround: int, line: OrderedDict
    ) -> None:
        """
        Creates a new DatamapLine object in the database. If
        _turnaround value is 0, the existing objects are retained
        in an instance variable for rollback upon exception.
        :param _timeround:
        :type _timeround: int
        :param line:
        :type line: collections.OrderedDict
        :return:
        :rtype: None
        """
        if _timeround == 0:
            for dml in self.datamap.datamapline_set.all():
                self._existing_dmls_cache.append(dml)
            DatamapLine.objects.filter(datamap=self.datamap).delete()
        dml = DatamapLine.objects.create(
            datamap=self.datamap,
            key=line["key"],
            sheet=line["sheet"],
            cell_ref=line["cell_ref"],
        )
        self._tmp_registered_dml_ids.append(dml.id)

    def _send_errors_to_messages(self, request, form) -> None:
        """
        Helper function to put a string in a Message object for
        later processing in the view template.
        :param request:
        :type request: django.core.handlers.wsgi.WSGIRequest
        :param form:
        :type form: datamap.forms.CSVForm
        :return:
        :rtype: None
        """
        for field, error in form.errors.items():
            messages.add_message(
                request,
                messages.ERROR,
                "Field: {} Errors: {}".format(field, ", ".join(error)),
            )

    def _parse_kwargs_to_error_string(self, kwargs: dict) -> str:
        err_lst = []
        err_stmt = []
        for x in kwargs.items():
            err_lst.append(x)
        for x in err_lst:
            err_stmt.append(f"{x[0]}: {x[1]}")
        return f"Database Error: {' '.join([x for x in err_stmt])} already appears in Datamap: {self.datamap}"
