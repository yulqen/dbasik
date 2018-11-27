from django.urls import path

from returns.views import FinancialQuartersList
from returns.views import ReturnDetail
from returns.views import ReturnLines
from . views import ReturnsList

app_name = "returns"

urlpatterns = [
    path("", ReturnsList.as_view(), name="returns_list"),
    path("return-data/<int:id>/", ReturnLines.as_view(), name="return_data"),
    path("financial-quarters/", FinancialQuartersList.as_view(), name="financial_quarters"),
    path("<int:pk>/", ReturnDetail.as_view(), name="returns_detail"),
]