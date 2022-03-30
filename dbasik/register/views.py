from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from collections import defaultdict

from .models import ProjectType, Tier, ProjectStage, StrategicAlignment, Project
from .forms import (
    ProjectTypeForm,
    TierForm,
    ProjectStageForm,
    StrategicAlignmentForm,
    ProjectForm,
)
from returns.models import ReturnItem


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = Project.objects.all()
        tiers = set([p.tier for p in projects])
        p_per_tier = defaultdict(list)
        for t in tiers:
            for p in projects:
                if p.tier == t:
                    p_per_tier[t].append(p)
        context["p_per_tier"] = p_per_tier.items()
        return context

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
        first = returns_for.first()
        returns_count = returns_for.count()
        if returns_count > 0:
            if ReturnItem.objects.filter(parent=first).count() > 1:
                context["returns"] = returns_for
                context["fq"] = returns_for.first().financial_quarter
                context["sro_full_name"] = first.data_by_key('SRO Full Name')['value_str']
                context["dca_narrative"] = first.data_by_key("Departmental DCA Narrative")['value_str']
                context["working_contact"] = first.data_by_key("Working Contact Name")['value_str']
                context["working_contact_phone"] = first.data_by_key("Working Contact Telephone")['value_str']
                context["dft_group"] = first.data_by_key("DfT Group")['value_str']
                # context["dft_division"] = first.data_by_key("DfT Division")['value_str']
                # context["rag"] = first.data_by_key("SRO assurance confidence RAG external")['value_str']
                # context["rag_c"] = self.rag_colours.get(first.data_by_key("SRO assurance confidence RAG external")['value_str'])
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
