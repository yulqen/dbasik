from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy, reverse

from . models import ProjectType, Tier, ProjectStage, StrategicAlignment, Project
from . forms import ProjectTypeForm, TierForm, ProjectStageForm, StrategicAlignmentForm, ProjectForm


class ProjectTypeDelete(DeleteView):
    model = ProjectType
    success_url = reverse_lazy("register:projecttype_list")


class ProjectTypeUpdate(UpdateView):
    model = ProjectType
    form_class = ProjectTypeForm
    template_name_suffix = "_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = ProjectType.objects.all()
        context['existing_objects'] = existing_objects
        return context


class ProjectTypeDetail(DetailView):
    model = ProjectType
    form_class = ProjectTypeForm


class ProjectTypeList(ListView):
    model = ProjectType


class ProjectTypeCreate(CreateView):
    model = ProjectType
    template_name_suffix = "_create"
    form_class = ProjectTypeForm
    success_url = reverse_lazy("register:projecttype_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = ProjectType.objects.all()
        context['existing_objects'] = existing_objects
        return context


class TierCreate(CreateView):
    model = Tier
    template_name_suffix = "_create"
    form_class = TierForm
    success_url = reverse_lazy("register:tier_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Tier.objects.all()
        context['existing_objects'] = existing_objects
        return context


class TierList(ListView):
    model = Tier


class TierDetail(DetailView):
    model = Tier


class TierDelete(DeleteView):
    model = Tier
    success_url = reverse_lazy("register:tier_list")


class TierUpdate(UpdateView):
    model = Tier
    form_class = TierForm
    template_name_suffix = "_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Tier.objects.all()
        context['existing_objects'] = existing_objects
        return context


class ProjectStageCreate(CreateView):
    model = ProjectStage
    template_name_suffix = "_create"
    form_class = ProjectStageForm
    success_url = reverse_lazy("register:projectstage_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = ProjectStage.objects.all()
        context['existing_objects'] = existing_objects
        return context


class ProjectStageList(ListView):
    model = ProjectStage


class ProjectStageDetail(DetailView):
    model = ProjectStage


class ProjectStageDelete(DeleteView):
    model = ProjectStage
    success_url = reverse_lazy("register:projectstage_list")


class ProjectStageUpdate(UpdateView):
    model = ProjectStage
    form_class = ProjectStageForm
    template_name_suffix = "_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = ProjectStage.objects.all()
        context['existing_objects'] = existing_objects
        return context


class StrategicAlignmentCreate(CreateView):
    model = StrategicAlignment
    template_name_suffix = "_create"
    form_class = StrategicAlignmentForm
    success_url = reverse_lazy("register:strategicalignment_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = StrategicAlignment.objects.all()
        context['existing_objects'] = existing_objects
        return context


class StrategicAlignmentList(ListView):
    model = StrategicAlignment


class StrategicAlignmentDetail(DetailView):
    model = StrategicAlignment


class StrategicAlignmentDelete(DeleteView):
    model = StrategicAlignment
    success_url = reverse_lazy("register:strategicalignment_list")


class StrategicAlignmentUpdate(UpdateView):
    model = StrategicAlignment
    form_class = StrategicAlignmentForm
    template_name_suffix = "_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = StrategicAlignment.objects.all()
        context['existing_objects'] = existing_objects
        return context



class ProjectCreate(CreateView):
    model = Project
    template_name_suffix = "_create"
    form_class = ProjectForm
    success_url = reverse_lazy("register:project_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Project.objects.all()
        context['existing_objects'] = existing_objects
        return context


class ProjectList(ListView):
    model = Project


class ProjectDetail(DetailView):
    model = Project


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy("register:project_list")


class ProjectUpdate(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name_suffix = "_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Project.objects.all()
        context['existing_objects'] = existing_objects
        return context
