from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy, reverse

from .models import ProjectType, Tier, ProjectStage, StrategicAlignment, Project
from .forms import (
    ProjectTypeForm,
    TierForm,
    ProjectStageForm,
    StrategicAlignmentForm,
    ProjectForm,
)
from returns.models import Return
from datamap.models import DatamapLine


class ProjectTypeDelete(LoginRequiredMixin, DeleteView):
    model = ProjectType
    success_url = reverse_lazy("register:projecttype_list")


class ProjectTypeUpdate(LoginRequiredMixin, UpdateView):
    model = ProjectType
    form_class = ProjectTypeForm
    template_name_suffix = "_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = ProjectType.objects.all()
        context["existing_objects"] = existing_objects
        return context


class ProjectTypeDetail(LoginRequiredMixin, DetailView):
    model = ProjectType
    form_class = ProjectTypeForm


class ProjectTypeList(LoginRequiredMixin, ListView):
    model = ProjectType


class ProjectTypeCreate(LoginRequiredMixin, CreateView):
    model = ProjectType
    template_name_suffix = "_create"
    form_class = ProjectTypeForm
    success_url = reverse_lazy("register:projecttype_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = ProjectType.objects.all()
        context["existing_objects"] = existing_objects
        return context


class TierCreate(LoginRequiredMixin, CreateView):
    model = Tier
    template_name_suffix = "_create"
    form_class = TierForm
    success_url = reverse_lazy("register:tier_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Tier.objects.all()
        context["existing_objects"] = existing_objects
        return context


class TierList(LoginRequiredMixin, ListView):
    model = Tier


class TierDetail(LoginRequiredMixin, DetailView):
    model = Tier


class TierDelete(LoginRequiredMixin, DeleteView):
    model = Tier
    success_url = reverse_lazy("register:tier_list")


class TierUpdate(LoginRequiredMixin, UpdateView):
    model = Tier
    form_class = TierForm
    template_name_suffix = "_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Tier.objects.all()
        context["existing_objects"] = existing_objects
        return context


class ProjectStageCreate(LoginRequiredMixin, CreateView):
    model = ProjectStage
    template_name_suffix = "_create"
    form_class = ProjectStageForm
    success_url = reverse_lazy("register:projectstage_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = ProjectStage.objects.all()
        context["existing_objects"] = existing_objects
        return context


class ProjectStageList(LoginRequiredMixin, ListView):
    model = ProjectStage


class ProjectStageDetail(LoginRequiredMixin, DetailView):
    model = ProjectStage


class ProjectStageDelete(LoginRequiredMixin, DeleteView):
    model = ProjectStage
    success_url = reverse_lazy("register:projectstage_list")


class ProjectStageUpdate(LoginRequiredMixin, UpdateView):
    model = ProjectStage
    form_class = ProjectStageForm
    template_name_suffix = "_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = ProjectStage.objects.all()
        context["existing_objects"] = existing_objects
        return context


class StrategicAlignmentCreate(LoginRequiredMixin, CreateView):
    model = StrategicAlignment
    template_name_suffix = "_create"
    form_class = StrategicAlignmentForm
    success_url = reverse_lazy("register:strategicalignment_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = StrategicAlignment.objects.all()
        context["existing_objects"] = existing_objects
        return context


class StrategicAlignmentList(LoginRequiredMixin, ListView):
    model = StrategicAlignment


class StrategicAlignmentDetail(LoginRequiredMixin, DetailView):
    model = StrategicAlignment


class StrategicAlignmentDelete(LoginRequiredMixin, DeleteView):
    model = StrategicAlignment
    success_url = reverse_lazy("register:strategicalignment_list")


class StrategicAlignmentUpdate(LoginRequiredMixin, UpdateView):
    model = StrategicAlignment
    form_class = StrategicAlignmentForm
    template_name_suffix = "_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = StrategicAlignment.objects.all()
        context["existing_objects"] = existing_objects
        return context


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    template_name_suffix = "_create"
    form_class = ProjectForm
    success_url = reverse_lazy("register:project_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Project.objects.all()
        context["existing_objects"] = existing_objects
        return context


class ProjectList(LoginRequiredMixin, ListView):
    model = Project

    def get_queryset(self):
        qs = Project.objects.all().order_by("name")
        return qs


class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project

    rag_colours = {
        "Amber": "eab735",
        "Green": "3d7f2b",
        "Amber/Green": "98aa3f"
    }


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        returns_for = self.object.return_projects.all().order_by("-financial_quarter")
        if len(returns_for) > 0:
            _all_data = returns_for.first().return_returnitems.all().values()
            if len(_all_data) > 1:
                context["fq"] = returns_for.first().financial_quarter
                _latest_return = {
                    DatamapLine.objects.get(id=item["datamapline_id"]).key: {
                        "value_str": item["value_str"],
                        "value_int": item["value_int"],
                        "value_float": item["value_float"],
                        "value_d ate": item["value_date"],
                        "value_datetime": item["value_datetime"],
                    }
                    for item in _all_data
                }
                context["sro_full_name"] = _latest_return['SRO Full Name']['value_str']
                context["rag"] = _latest_return["SRO assurance confidence RAG external"]['value_str']
                context["rag_c"] = self.rag_colours.get(_latest_return["SRO assurance confidence RAG external"]['value_str'])
                return context
            else:
                return context
        else:
            return context


class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy("register:project_list")


class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name_suffix = "_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Project.objects.all()
        context["existing_objects"] = existing_objects
        return context
