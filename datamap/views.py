from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView

from .forms import CreateDatamapForm, UploadDatamap
from .models import Datamap, DatamapLine, PortfolioFamily
from exceptions import IllegalFileUpload, IncorrectHeaders
from helpers import CSVUploadedFile


class DatamapList(ListView):
    model = Datamap


def datamap_view(request, dm_pk):
    dm_lines = DatamapLine.objects.filter(datamap_id=dm_pk).order_by("id")
    context = {"dm_lines": dm_lines}
    return render(request, "datamap/datamap.html", context)


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
            return HttpResponseRedirect("/admin")
    else:
        form = CreateDatamapForm()

    return render(request, "datamap/create_datamap.html", {"form": form})


def upload_datamap(request):
    if request.method == "POST":
        form = UploadDatamap(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES["uploaded_file"])
            f = request.FILES["uploaded_file"]
            print(type(f))
            # pass to the file handler
            if f.content_type == "text/csv":
                try:
                    CSVUploadedFile(f).process()
                except IllegalFileUpload:  # TODO: implement this - was removed in refactor
                    messages.add_message(request, messages.INFO, "Illegal file type")
                except IncorrectHeaders as e:
                    messages.add_message(request, messages.INFO, e.args[0])
        elif form.errors:
            for v in form.errors.values():
                messages.add_message(request, messages.INFO, v)

    else:
        form = UploadDatamap()

    return render(request, "datamap/upload_datamap.html", {"form": form})
