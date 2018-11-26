from django.urls import path

from returns.views import FinancialQuartersList
from returns.views import ReturnsDetail
from . views import ReturnsList

app_name = "returns"

urlpatterns = [
    path("", ReturnsList.as_view(), name="returns_list"),
    path("financial-quarters/", FinancialQuartersList.as_view(), name="financial_quarters"),
    path("<int:pk>/", ReturnsDetail.as_view(), name="returns_detail"),
]