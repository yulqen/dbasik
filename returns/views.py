from django.views.generic import DetailView
from django.views.generic import ListView

from register.models import FinancialQuarter
from returns.models import Return
from returns.models import ReturnItem


class ReturnsList(ListView):
    queryset = Return.objects.all()
    template_name = "returns/returns_list.html"


class ReturnLines(ListView):
    model = ReturnItem
    paginate_by = 100

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["return"] = Return.objects.get(id=self.kwargs["id"])
        return context


class ReturnDetail(DetailView):
    model = Return


class FinancialQuartersList(ListView):
    queryset = FinancialQuarter.objects.all()
