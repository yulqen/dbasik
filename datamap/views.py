import csv
import logging
import re
from typing import List

from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from datamap.helpers import _parse_kwargs_to_error_string
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
        self.errors = []
        self._tmp_registered_dml_ids = []

    def post(self, request, *args, **kwargs):
        dm = Datamap.objects.get(slug=kwargs["slug"])
        form = self.get_form()
        self._tmp_registered_dml_ids = []
        if form.is_valid():
            reader = csv.DictReader(
                x.decode("utf-8") for x in request.FILES["uploaded_file"].readlines()
            )
            for line in reader:
                form = CSVForm(line)
                if form.is_valid():
                    try:
                        dml = DatamapLine.objects.create(
                            datamap=dm,
                            key=line["key"],
                            sheet=line["sheet"],
                            cell_ref=line["cell_ref"],
                        )
                        self._tmp_registered_dml_ids.append(dml.id)
                    except IntegrityError:
                        err_str = _parse_kwargs_to_error_string(dm, line)
                        messages.add_message(request, messages.ERROR, err_str)
                        [DatamapLine.objects.get(id=dm_id).delete() for dm_id in self._tmp_registered_dml_ids]
                        self._tmp_registered_dml_ids = []
                        return self.form_invalid(form)
                    except ValueError:
                        self.send_errors_to_messages(form, request)
                        return self.form_invalid(form)
                else:
                    self.send_errors_to_messages(form, request)
                    return self.form_invalid(form)
            return self.form_valid(form)

        else:
            self.send_errors_to_messages(form, request)
            return self.form_invalid(form)

    def send_errors_to_messages(self, form, request):
        for field, error in form.errors.items():
            messages.add_message(
                request,
                messages.ERROR,
                "Field: {} Errors: {}".format(field, ", ".join(error)),
            )
