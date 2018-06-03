import csv
import codecs

from django.utils.text import slugify
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import (
    UploadDatamap,
    DatamapForm,
    DatamapLineForm,
    DatamapLineEditForm,
    DatamapLineDeleteForm,
    CSVForm,
)
from .models import Datamap, DatamapLine
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
#   success_url = reverse_lazy("datamaps:uploaddatamap", )

    def get_success_url(self, **kwargs):
        name_field = self.request.POST['name']
        tier_id = self.request.POST['tier']
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
#       dm_slug = get_object_or_404(DatamapLine, pk=self.kwargs['pk']).datamap.slug
        return reverse("datamaps:datamap_detail", kwargs={'pk': self.object.pk})



class DatamapLineDelete(DeleteView):
    model = DatamapLine
    success_url = reverse_lazy("datamaps:datamap_list")


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


def upload_datamap(request, slug):

    errors = []

    if request.method == "POST":
        form = UploadDatamap(request.POST, request.FILES)
        if form.is_valid():
            dm = get_object_or_404(Datamap, slug=slug)
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
                        if replace is True:
                            DatamapLine.objects.filter(
                                datamap=dm, key=csv_form.cleaned_data["key"]
                            ).delete()
                            try:
                                _process(row, dm)
                            except IntegrityError as err:
                                messages.add_message(request, messages.ERROR, err)
                                return render(
                                    request,
                                    "datamap/upload_datamap.html",
                                    {"form": form},
                                )
                        else:
                            try:
                                _process(row, dm)
                            except IntegrityError as err:
                                messages.add_message(request, messages.ERROR, err)
                                return render(
                                    request,
                                    "datamap/upload_datamap.html",
                                    {"form": form},
                                )
                    else:
                        for field, error in csv_form.errors.items():
                            messages.add_message(
                                request,
                                messages.ERROR,
                                "Field: {} Errors: {}".format(field, ", ".join(error)),
                            )
                        DatamapLine.objects.filter(datamap=dm).delete()
                        return render(
                            request, "datamap/upload_datamap.html", {"form": form}
                        )
                    if not csv_form.is_valid():
                        for e in csv_form.errors.items():
                            errors.append(e)
                return HttpResponseRedirect(reverse("datamaps:datamap_list"))

        elif form.errors:
            for v in form.errors.values():
                messages.add_message(request, messages.INFO, v)

    else:
        form = UploadDatamap()

    return render(request, "datamap/upload_datamap.html", {"form": form})
