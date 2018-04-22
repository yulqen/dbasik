from django.shortcuts import render
from django.views.generic import ListView
from .models import Datamap


class DatamapList(ListView):
    model = Datamap
