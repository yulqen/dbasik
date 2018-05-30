from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from . models import ProjectType
from . forms import ProjectTypeForm


class ProjectTypeDelete(DeleteView):
    model = ProjectType
    success_url = reverse_lazy("register:projecttype_list")


class ProjectTypeUpdate(UpdateView):
    model = ProjectType
    form_class = ProjectTypeForm
    template_name_suffix = "_update_form"


class ProjectTypeDetail(DetailView):
    model = ProjectType
    form_class = ProjectTypeForm


class ProjectTypeList(ListView):
    model = ProjectType


class ProjectTypeCreate(CreateView):
    model = ProjectType
    template_name_suffix = "_create_form"
    form_class = ProjectTypeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = ProjectType.objects.all()
        context['existing_objects'] = existing_objects
        return context

