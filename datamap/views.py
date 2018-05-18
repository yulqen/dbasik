from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse
from django.conf import settings

from .forms import CreateDatamapForm, UploadDatamap
from .models import Datamap, DatamapLine, PortfolioFamily
from exceptions import IllegalFileUpload, IncorrectHeaders, DatamapLineValidationError
from helpers import CSVUploadedFile, delete_datamap


class DatamapList(ListView):
    model = Datamap


def datamap_view(request, dm_pk):
    dm_lines = DatamapLine.objects.filter(datamap_id=dm_pk).order_by("id")
    dm_name = Datamap.objects.get(pk=dm_pk).name
    dm = Datamap.objects.get(pk=dm_pk)
    context = {"dm_lines": dm_lines, "dm_name": dm_name, "dm": dm}
    return render(request, "datamap/datamap.html", context)


def delete_datamap_view(request, dm_pk: int):
    dm = Datamap.objects.get(pk=dm_pk)
    delete_datamap(dm)
    return HttpResponseRedirect("/datamaps")


def create_datamap(request):
    if request.method == "POST":
        form = CreateDatamapForm(request.POST)
        if form.is_valid():
            print(f"We received {form.cleaned_data}")
            name = form.cleaned_data["name"]
            portfolio_family = form.cleaned_data["portfolio_family"]
            pf_obj = PortfolioFamily.objects.get(pk=portfolio_family)
            new_dm = Datamap(name=name, portfolio_family=pf_obj)
            new_dm.save()
            return HttpResponseRedirect("/uploaddatamap")
    else:
        form = CreateDatamapForm()
        # list of current datamaps
        dms_l = Datamap.objects.all()

    return render(request, "datamap/create_datamap.html", {"form": form, 'dms_l': dms_l})


def upload_datamap(request):

    field_keys = settings.DATAMAP_FIELD_KEYS

    if request.method == "POST":
        form = UploadDatamap(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES["uploaded_file"]
            given_name = request.POST["file_name"]
            dm = request.POST["target_datamap"]
            if "replace_all_entries" in request.POST:
                replace = request.POST["replace_all_entries"]
            else:
                replace = "off"
            if f.content_type == "text/csv":
                try:
                    CSVUploadedFile(f, given_name, dm, field_keys, replace).process()
                    return HttpResponseRedirect(reverse("datamap", args=[dm]))
                except IllegalFileUpload:  # TODO: implement this - was removed in refactor
                    messages.add_message(request, messages.INFO, "Illegal file type")
                except IncorrectHeaders as e:
                    messages.add_message(request, messages.INFO, e.args[0])
                except DatamapLineValidationError as e:
                    msg = (
                        f"Validation error in field: {e.args[0][0].error_field}\n"
                        f"{e.args[0][0].django_validator_message} {e.args[0][0].field_given_value}"
                    )
                    messages.add_message(request, messages.INFO, msg)

        elif form.errors:
            for v in form.errors.values():
                messages.add_message(request, messages.INFO, v)

    else:
        form = UploadDatamap()

    return render(
        request, "datamap/upload_datamap.html", {"form": form, "field_keys": field_keys}
    )
