from django.views.generic import DetailView
from django.views.generic import ListView

from register.models import FinancialQuarter
from returns.models import ReturnItem


class ReturnsList(ListView):
    queryset = ReturnItem.objects.all()


class ReturnsDetail(DetailView):
    model = ReturnItem


class FinancialQuartersList(ListView):
    queryset = FinancialQuarter.objects.all()
