from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from .models import Datamap, DatamapLine
from .forms import CreateDatamapForm


class DatamapList(ListView):
    model = Datamap


def datamap_view(request, dm_pk):
    dm_lines = DatamapLine.objects.filter(datamap_id=dm_pk)
    context = {'dm_lines': dm_lines}
    return render(request, 'datamap/datamap.html', context)


def create_datamap(request):
    if request.method == 'POST':
        form = CreateDatamapForm(request.POST)
        if form.is_valid():
            print(f"We received {form.cleaned_data}")
            name = form.cleaned_data['name']
            portfolio_family = form.cleaned_data['portfolio_family']
            return HttpResponseRedirect('/admin')
    else:
        form = CreateDatamapForm()

    return render(request, 'datamap/create_datamap.html', {'form': form})
