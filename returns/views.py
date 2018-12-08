import os
from typing import List

from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView
from openpyxl import load_workbook

from excelparser.helpers.parser import ParsedSpreadsheet
from register.models import FinancialQuarter, Project
from returns.forms import ReturnBatchCreateForm, ReturnCreateForm
from returns.helpers import generate_master
from returns.models import Return, ReturnItem


class ReturnBatchCreate(LoginRequiredMixin, FormView):
    form_class = ReturnBatchCreateForm
    template_name = "returns/return_batch_create.html"
    success_url = reverse_lazy("returns:returns_list")

    def form_valid(self, form):
        fq = form.cleaned_data['financial_quarter']
        datamap = form.cleaned_data['datamap']
        files = self.request.FILES.getlist('source_files')
        for f in files:
            datamap = form.cleaned_data['datamap']
            save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', f.name)
            path = default_storage.save(save_path, f)
            project = Project.objects.get(name=f.name.strip(".xlsm"))
            return_obj = Return.objects.create(
                project=project,
                financial_quarter=fq
            )
            parsed_spreadsheet = ParsedSpreadsheet(path, project, return_obj, datamap)
            parsed_spreadsheet.process()
        return HttpResponseRedirect(self.get_success_url())


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
    file_name = f"Master_for_Q{fq.quarter}_{fq.year}.xlsm"
    generate_master(fq, file_name, datamap)
    with open(file_name, "rb") as excel:
        data = excel.read()
        response = HttpResponse(data, content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = f"attachment; filename={file_name}"
        return response


class ReturnsList(LoginRequiredMixin, ListView):
    queryset = Return.objects.all()
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
