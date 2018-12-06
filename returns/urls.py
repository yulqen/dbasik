from django.urls import path
from django.views.decorators.cache import cache_page

from returns.views import FinancialQuartersList
from returns.views import ReturnCreate
from returns.views import ReturnDetail
from returns.views import ReturnLines
from . views import ReturnsList

app_name = "returns"

urlpatterns = [
    path("", ReturnsList.as_view(), name="returns_list"),
#   path("return-data/<int:id>/", cache_page(60 * 15)(ReturnLines.as_view()), name="return_data"),
    path("return-data/<int:id>/", ReturnLines.as_view(), name="return_data"),
    path("create/", ReturnCreate.as_view(), name="return_create"),
    path("financial-quarters/", FinancialQuartersList.as_view(), name="financial_quarters"),
    path("<int:pk>/", ReturnDetail.as_view(), name="returns_detail"),
]
