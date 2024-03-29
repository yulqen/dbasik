import logging
import os
import tempfile
from typing import List

# from dbasik.excelparser.helpers.parser import ParsedSpreadsheet
from dbasik.register.models import FinancialQuarter, Project
from dbasik.returns.forms import ReturnBatchCreateForm, ReturnCreateForm
from dbasik.returns.helpers import generate_master
from dbasik.returns.models import Return, ReturnItem
from dbasik.returns.tasks import process_batch as process
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView
from rest_framework import viewsets

from .serializers import ReturnItemSerializer, ReturnSerializer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# API viewsets


class ReturnViewSet(viewsets.ModelViewSet):
    queryset = Return.objects.all()
    serializer_class = ReturnSerializer


class ReturnItemViewSet(viewsets.ModelViewSet):
    queryset = ReturnItem.objects.all()
    serializer_class = ReturnItemSerializer


# class ReturnItemViewSet(viewsets.ModelViewSet):
#     queryset = Datamap.objects.all()
#     serializer_class = DatamapSerializer


class DeleteReturn(LoginRequiredMixin, DeleteView):
    model = Return
    success_url = reverse_lazy("returns:returns_list")


class ReturnBatchCreate(LoginRequiredMixin, FormView):
    form_class = ReturnBatchCreateForm
    template_name = "returns/return_batch_create.html"
    success_url = reverse_lazy("returns:returns_list")

    def get_form_kwargs(self):
        self.kwargs = super().get_form_kwargs()
        self.valid_project_names = [
            p.name for p in Project.objects.all().order_by("name")
        ]
        self.kwargs["valid_project_names"] = self.valid_project_names
        return self.kwargs

    def get_context_data(self, **kwargs):
        """
        We want to provide a list of valid project names, and the
        projects themselves.
        """
        context = super().get_context_data(**kwargs)
        projects = Project.objects.all().order_by("name")
        context["projects"] = projects
        return context

    def form_valid(self, form):
        files = self.request.FILES.getlist("source_files")
        logger.info(f"files is: {files}")
        # test if we have erroneous files
        for uploaded_file in files:
            uploaded_file = uploaded_file.name.split(".")[0]
            logger.info(f"Uploaded file is {uploaded_file}")
            if uploaded_file not in self.valid_project_names:
                logger.info(f"Split file name is {uploaded_file}")
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    f"{uploaded_file} is not a valid filename in this context.",
                )
                return redirect("returns:returns_list")
        fq_id = form.cleaned_data["financial_quarter"].id
        dm_id = form.cleaned_data["datamap"].id
        for f in files:
            project_name = f.name.split(".")[0]
            save_path = os.path.join(settings.MEDIA_ROOT, "uploads", str(f))
            default_storage.save(save_path, f)
            process.delay(fq_id, dm_id, save_path, project_name)
        messages.success(
            self.request, "Processing uploads - please refresh page later..."
        )
        return redirect("returns:returns_list")

    # def form_valid(self, form):
    #     fq = form.cleaned_data['financial_quarter']
    #     datamap = form.cleaned_data['datamap']
    #     files = self.request.FILES.getlist('source_files')
    #     for f in files:
    #         datamap = form.cleaned_data['datamap']
    #         save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', f.name)
    #         path = default_storage.save(save_path, f)
    #         project = Project.objects.get(name=f.name.strip(".xlsm"))
    #         return_obj = Return.objects.create(
    #             project=project,
    #             financial_quarter=fq
    #         )
    #         parsed_spreadsheet = ParsedSpreadsheet(path, project, return_obj, datamap)
    #         parsed_spreadsheet.process()
    #     return HttpResponseRedirect(self.get_success_url())


def download_master(request, fqid: int):
    fq = FinancialQuarter.objects.get(pk=fqid)

    # TODO - for now we assume the datamap is the same
    # for all returns, but as long as we allow uploading
    # of seperate returns, the datamap could be different
    # which will produce a bad master using this process.
    # Will be fixed by only allowing batch upload of templates
    # when making returns.
    return_obj_sample = fq.return_financial_quarters.first()
    first_return_obj_item = return_obj_sample.return_returnitems.first()
    datamap = first_return_obj_item.datamapline.datamap
    file_name = f"Master_for_Q{fq.quarter}_{fq.year}.xlsx"

    # TODO - test if downloads is there and if not, create it
    save_path = os.path.join(tempfile.mkdtemp(), file_name)
    generate_master(fq, save_path, datamap)
    with open(save_path, "rb") as excel:
        data = excel.read()
        response = HttpResponse(data, content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = f"attachment; filename={file_name}"
        return response


class ReturnsList(LoginRequiredMixin, ListView):
    queryset = Return.objects.all().order_by("project__name")
    template_name = "returns/returns_list.html"

    def get_context_data(self, **kwargs):
        """
        We want to add in a list of FinancialYear objects that contain
        Return items.
        """
        context = super().get_context_data(**kwargs)
        valid_fqs: List[FinancialQuarter] = []
        for fq in FinancialQuarter.objects.all():
            if len(fq.return_financial_quarters.all()) > 0:
                valid_fqs.append(fq)
        if valid_fqs:
            valid_fqs = reversed(sorted(valid_fqs, key=lambda x: x.start_date))
            context.update({"valid_fqs": valid_fqs})
            return context
        else:
            return context


class ReturnCreate(LoginRequiredMixin, CreateView):
    model = Return
    form_class = ReturnCreateForm
    template_name = "returns/return_create.html"


class ReturnLines(LoginRequiredMixin, ListView):
    model = ReturnItem

    def get_queryset(self):
        this_return = Return.objects.get(id=self.kwargs["id"])
        qs = this_return.return_returnitems.all().order_by("datamapline")
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["return"] = Return.objects.get(id=self.kwargs["id"])
        return context


class ReturnDetail(LoginRequiredMixin, DetailView):
    model = Return


class FinancialQuartersList(LoginRequiredMixin, ListView):
    queryset = FinancialQuarter.objects.all()
