import csv
import logging
from collections import OrderedDict

from dbasik.datamap.helpers import parse_kwargs_to_error_string
from dbasik.register.models import Tier
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.forms import Form
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView

from .forms import (
    CSVForm,
    DatamapForm,
    DatamapLineEditForm,
    DatamapLineForm,
    UploadDatamap,
)
from .models import Datamap, DatamapLine

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DatamapDelete(LoginRequiredMixin, DeleteView):
    model = Datamap
    success_url = reverse_lazy("datamaps:datamap_list")


class DatamapUpdate(LoginRequiredMixin, UpdateView):
    model = Datamap
    template_name_suffix = "_update"
    form_class = DatamapForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Datamap.objects.all()
        context["existing_objects"] = existing_objects
        return context


class DatamapCreate(LoginRequiredMixin, CreateView):
    model = Datamap
    template_name_suffix = "_create"
    form_class = DatamapForm

    def get_success_url(self, **kwargs):
        name_field = self.request.POST["name"]
        # tier_id = self.request.POST["tier"]
        # tier_name = get_object_or_404(Tier, pk=tier_id).name
        slugged = slugify(name_field)
        return reverse_lazy("datamaps:uploaddatamap", args=[slugged])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Datamap.objects.all()
        context["existing_objects"] = existing_objects
        return context


@login_required
def datamap_detail(request, slug: str):
    dm_lines = DatamapLine.objects.filter(datamap__slug=slug).order_by("id")
    dms = Datamap.objects.all()
    dm_name = Datamap.objects.get(slug=slug).name
    dm = get_object_or_404(Datamap, slug=slug)
    context = {"dms": dms, "dm_lines": dm_lines, "dm_name": dm_name, "dm": dm}
    return render(request, "datamap/datamap_detail.html", context)


class DatamapList(LoginRequiredMixin, ListView):
    model = Datamap


class DatamapLineCreate(LoginRequiredMixin, CreateView):
    model = DatamapLine
    form_class = DatamapLineForm

    def get_context_data(self, **kwargs):
        dm = Datamap.objects.get(slug=self.kwargs["slug"])
        kwargs["datamap"] = dm
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["datamap_id"] = Datamap.objects.get(slug=self.kwargs["slug"]).id
        return kwargs

    def get_success_url(self):
        return reverse("datamaps:datamap_detail", args=[self.kwargs["slug"]])


class DatamapLineUpdate(LoginRequiredMixin, UpdateView):
    model = DatamapLine
    form_class = DatamapLineEditForm

    def get_success_url(self):
        dm_slug = get_object_or_404(DatamapLine, pk=self.kwargs["pk"]).datamap.slug
        #       return reverse("datamaps:datamapline_detail", kwargs={'pk': self.object.pk})
        return reverse("datamaps:datamap_detail", kwargs={"slug": dm_slug})


class DatamapLineDelete(LoginRequiredMixin, DeleteView):
    model = DatamapLine

    def get_success_url(self):
        dm_slug = get_object_or_404(DatamapLine, pk=self.kwargs["pk"]).datamap.slug
        return reverse("datamaps:datamap_detail", kwargs={"slug": dm_slug})


# noinspection Pylint
class UploadDatamapView(LoginRequiredMixin, FormView):
    template_name = "datamap/upload_datamap.html"
    form_class = UploadDatamap

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.datamap: Datamap = None
        self.errors: list = []
        self._ids_of_just_created_datamaplines: list = []
        self._temporary_datamapline_objects: list = []

    def get_success_url(self):
        return reverse_lazy("datamaps:datamap_detail", args=[self.kwargs["slug"]])

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

        # TODO: catch the UnicodeDecodeError here. We can't wrap a try Except
        # around this in its current form due to the generator exp.
        reader = csv.DictReader(x.decode("utf-8") for x in uploaded_file_data)
        _timeround = 0
        for line in reader:
            #   line.pop("")
            csv_form = CSVForm(line)
            if csv_form.is_valid():
                try:
                    self._create_new_dml_with_line_from_csv(_timeround, line)
                except IntegrityError:
                    self._add_database_error_to_messages(request, line)
                    #                   return self.form_valid(main_form)
                    continue
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
        err_str = parse_kwargs_to_error_string(self.datamap, line)
        messages.add_message(request, messages.ERROR, err_str)

    #       self._rollback_database()

    def _rollback_database(self) -> None:
        """
        Deletes all DatamapLine objects in list of just-created objects.
        :return: None
        :rtype: None
        """
        [
            DatamapLine.objects.get(id=dm_id).delete()
            for dm_id in self._ids_of_just_created_datamaplines
        ]
        for x in self._temporary_datamapline_objects:
            x.save()
        self._reset_caches()

    def _reset_caches(self) -> None:
        """
        Sets temporary cache lists back to empty lists.
        :return:
        :rtype:
        """
        self._ids_of_just_created_datamaplines = []
        self._temporary_datamapline_objects = []

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
            for dml in self.datamap.datamaplines.all():
                self._temporary_datamapline_objects.append(dml)
            DatamapLine.objects.filter(datamap=self.datamap).delete()
        dml = DatamapLine.objects.create(
            datamap=self.datamap,
            key=line["key"],
            sheet=line["sheet"],
            cell_ref=line["cell_ref"],
        )
        self._ids_of_just_created_datamaplines.append(dml.id)

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
