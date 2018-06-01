import csv
import codecs

from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import (
    CreateDatamapForm,
    UploadDatamap,
    EditDatamapLineForm,
    DatamapForm,
    DatamapLineForm,
    CSVForm,
)
from .models import Datamap, DatamapLine
from exceptions import IllegalFileUpload, IncorrectHeaders, DatamapLineValidationError
from helpers import CSVUploadedFile, delete_datamap
from register.models import Tier


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
    success_url = reverse_lazy("datamaps:uploaddatamap")

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


def datamap_delete(request, slug):
    dm = get_object_or_404(Datamap, slug=slug)
    delete_datamap(dm)
    return HttpResponseRedirect("/datamaps")


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


def datamapline_update(request, dml_pk):
    instance = get_object_or_404(DatamapLine, pk=dml_pk)
    if request.method == "POST":
        form = EditDatamapLineForm(request.POST, instance)
        if form.is_valid():
            key = form.cleaned_data["key"]
            sheet = form.cleaned_data["sheet"]
            cell_ref = form.cleaned_data["cell_ref"]
            slug = instance.datamap.slug
            existing_dml = DatamapLine.objects.get(pk=dml_pk)
            existing_dml.key = key
            existing_dml.sheet = sheet
            existing_dml.cell_ref = cell_ref
            existing_dml.save()
            return HttpResponseRedirect(f"/datamaps/{slug}")
    else:
        instance_data = {
            "key": instance.key, "sheet": instance.sheet, "cell_ref": instance.cell_ref
        }
        form = EditDatamapLineForm(instance_data)

    return render(
        request, "datamap/edit_datamapline.html", {"form": form, "dml_pk": dml_pk}
    )


def _process(row, dm_instance):
    """Save datamap line to database.
    """
    dml = DatamapLine(
        datamap=dm_instance,
        key=row["key"],
        sheet=row["sheet"],
        cell_ref=row["cell_ref"],
    )
    dml.save()


def upload_datamap(request):

    errors = []

    if request.method == "POST":
        form = UploadDatamap(request.POST, request.FILES)
        if form.is_valid():
            dm = form.cleaned_data["target_datamap"]
            slug = dm.slug
            csv_file = request.FILES["uploaded_file"]
            if "replace_all_entries" in request.POST:
                replace = form.cleaned_data["replace_all_entries"]
            else:
                replace = "off"
            if csv_file.content_type == "text/csv":
                csv_reader = csv.DictReader(codecs.iterdecode(csv_file, "utf-8"))
                for row in csv_reader:
                    csv_form = CSVForm(row)
                    if csv_form.is_valid():
                        if replace == "on":
                            DatamapLine.objects.filter(datamap=dm, key=form.cleaned_data['key']).delete()
                            _process(row, dm)
                        else:
                            _process(row, dm)
                    else:
                        for field, error in csv_form.errors.items():
                            if field == "key":
                                messages.add_message(request, messages.ERROR, "Field: {} Errors: {} Key: {}".format(field, ', '.join(error), row['key']))
                            else:
                                messages.add_message(request, messages.ERROR, "Field: {} Errors: {}".format(field, ', '.join(error)))
                            DatamapLine.objects.filter(datamap=dm).delete()
                        return render(request, "datamap/upload_datamap.html", {"form": form})
                    if not csv_form.is_valid():
                        for e in csv_form.errors.items():
                            errors.append(e)
                if errors:
                    for e in errors:
                        if e[0] == "key":
                            messages.add_message(request, messages.ERROR, "Field: {} Errors: {} Key: {}".format(e[0], ', '.join(e[1]), row['key']))
                        else:
                            messages.add_message(request, messages.ERROR, "Field: {} Errors: {}".format(e[0], ', '.join(e[1])))
                    return render(request, "datamap/upload_datamap.html", {"form": form})
                csv_reader = csv.DictReader(codecs.iterdecode(csv_file, "utf-8"))
                for row in csv_reader:
                    if csv_form.is_valid() and replace == "on":
                        dm_inst = Datamap.objects.get(pk=dm.id)
                        DatamapLine.objects.filter(datamap=dm_inst).delete()
                        _process(row, dm_inst)
                    elif csv_form.is_valid():
                        dm_inst = Datamap.objects.get(pk=dm.id)
                        _process(row, dm)

>>>>>>> develop

                return HttpResponseRedirect(reverse("datamaps:datamap_list"))

        elif form.errors:
            for v in form.errors.values():
                messages.add_message(request, messages.INFO, v)

    else:
        form = UploadDatamap()

    return render(request, "datamap/upload_datamap.html", {"form": form})
