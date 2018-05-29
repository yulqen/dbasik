from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from . models import ProjectType


class ProjectTypeDelete(DeleteView):
    model = ProjectType
    success_url = "/register/projecttype/"


class ProjectTypeDetail(DetailView):
    model = ProjectType


class ProjectTypeList(ListView):
    model = ProjectType


class ProjectTypeCreate(CreateView):
    model = ProjectType
    fields = ['name']
    template_name_suffix = "_create_form"
    success_url = "/register/projecttype/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = ProjectType.objects.all()
        context['existing_objects'] = existing_objects
        return context

