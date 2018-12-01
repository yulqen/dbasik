from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView

from register.models import FinancialQuarter
from returns.forms import ReturnCreateForm
from returns.models import Return
from returns.models import ReturnItem


class ReturnsList(LoginRequiredMixin, ListView):
    queryset = Return.objects.all()
    template_name = "returns/returns_list.html"


class ReturnCreate(LoginRequiredMixin, CreateView):
    model = Return
    form_class = ReturnCreateForm
    success_url = reverse_lazy("returns:returns_list")
    template_name = "returns/return_create.html"


class ReturnLines(LoginRequiredMixin, ListView):
    model = ReturnItem
    paginate_by = 100

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["return"] = Return.objects.get(id=self.kwargs["id"])
        return context


class ReturnDetail(LoginRequiredMixin, DetailView):
    model = Return


class FinancialQuartersList(LoginRequiredMixin, ListView):
    queryset = FinancialQuarter.objects.all()
