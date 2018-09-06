import logging
import re
from typing import List

from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from datamap.helpers import DatamapLinesFromCSVFactory
from .forms import UploadDatamap, DatamapForm, DatamapLineForm, DatamapLineEditForm
from .models import Datamap, DatamapLine
from register.models import Tier

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
    #   success_url = reverse_lazy("datamaps:uploaddatamap", )

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


# datamapline view functions


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


class UploadDatamapView(FormView):
    template_name = "datamap/upload_datamap.html"
    form_class = UploadDatamap
    success_url = reverse_lazy("datamaps:datamap_list")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        dm = Datamap.objects.get(slug=kwargs["slug"])
        form = self.get_form()
        if form.is_valid():
            factory = DatamapLinesFromCSVFactory(dm, request.FILES["uploaded_file"])
            try:
                factory.process()
            except IntegrityError:
                # TODO fix this, it doesn't show the IntegrityError
                # Problem is, there are two types of error I need to handle:
                #   - form errors (validation on form fields)
                #   - other errors, such as IntegrityError, which is thrown
                # at the database level.
                # Django patterns already handle ValidationErrors via form.is_valid()
                # and form.valid_form() and form.invalid_form(), so I need to use those
                # but the IntegrityErrors are something I need to handle separately.
                # TODO research ways to write own Exception handlers in Django
                form.add_error(None, ValidationError("Baws!"))
            except ValueError:
                for field, error in factory.errors.items():
                    messages.add_message(
                        request,
                        messages.ERROR,
                        "Field: {} Errors: {}".format(field, ", ".join(error)),
                    )
                return self.form_invalid(form)
            return self.form_valid(form)


# def upload_datamap(request, slug):
#
#     acceptable_content = settings.ACCEPTABLE_CONTENT
#     errors = []
#     integrity_error_messages = []
#
#     if request.method == "POST":
#         form = UploadDatamap(request.POST, request.FILES)
#         if form.is_valid():
#             dm = get_object_or_404(Datamap, slug=slug)
#             csv_file = request.FILES["uploaded_file"]
#             logger.info(f"Filetype {csv_file.content_type} uploaded")
#             logger.info(f"Acceptable is: {acceptable_content}")
#             if csv_file.content_type in acceptable_content:
#                 csv_reader = csv.DictReader(codecs.iterdecode(csv_file, "utf-8"))
#                 for row in csv_reader:
#                     csv_form = CSVForm(row)
#                     if csv_form.is_valid():
#                         if form.cleaned_data["replace_all_entries"] is True:
#                             DatamapLine.objects.filter(
#                                 datamap=dm, key=csv_form.cleaned_data["key"]
#                             ).delete()
#                             try:
#                                 # try to save in database
#                                 _process(row, dm)
#                             except IntegrityError as err:
#                                 # cannot save due to integrity error
#                                 # we're going to collage the error messages and save them for later
#                                 integrity_error_messages.append(err)
#                                 continue
#                             if integrity_error_messages:
#                                 # we have accumulated errors, so now add them to messages
#                                 _add_integrity_errors_to_messages(
#                                     request, dm, integrity_error_messages
#                                 )
#                                 return render(
#                                     request,
#                                     "datamap/upload_datamap.html",
#                                     {"form": form},
#                                 )
#                         else:
#                             try:
#                                 # try to save in database
#                                 _process(row, dm)
#                             except IntegrityError as err:
#                                 # cannot save due to integrity error
#                                 # we're going to collage the error messages and save them for later
#                                 integrity_error_messages.append(err)
#                                 continue
#                             if integrity_error_messages:
#                                 # we have accumulated errors, so now add them to messages
#                                 _add_integrity_errors_to_messages(
#                                     request, dm, integrity_error_messages
#                                 )
#                                 return render(
#                                     request,
#                                     "datamap/upload_datamap.html",
#                                     {"form": form},
#                                 )
#                     else:
#                         for field, error in csv_form.errors.items():
#                             messages.add_message(
#                                 request,
#                                 messages.ERROR,
#                                 "Field: {} Errors: {}".format(field, ", ".join(error)),
#                             )
#                         DatamapLine.objects.filter(datamap=dm).delete()
#                         return render(
#                             request, "datamap/upload_datamap.html", {"form": form}
#                         )
#                     if not csv_form.is_valid():
#                         for e in csv_form.errors.items():
#                             errors.append(e)
#                 return HttpResponseRedirect(reverse("datamaps:datamap_list"))
#             else:
#                 messages.add_message(
#                     request,
#                     messages.ERROR,
#                     f"{csv_file.content_type} is not an acceptable CSV type. See documentation.",
#                 )
#
#         elif form.errors:
#             for v in form.errors.values():
#                 messages.add_message(request, messages.INFO, v)
#
#     else:
#         form = UploadDatamap()
#
#     return render(request, "datamap/upload_datamap.html", {"form": form})
