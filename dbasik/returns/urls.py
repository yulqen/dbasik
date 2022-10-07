from django.urls import path
from django.views.decorators.cache import cache_page

from dbasik.returns.views import FinancialQuartersList

# from returns.views import ReturnItem
from dbasik.returns.views import ReturnCreate
from dbasik.returns.views import ReturnBatchCreate
from dbasik.returns.views import ReturnDetail
from dbasik.returns.views import DeleteReturn
from dbasik.returns.views import ReturnLines
from .views import ReturnsList, download_master

app_name = "returns"

urlpatterns = [
    path("", ReturnsList.as_view(), name="returns_list"),
    #   path("return-data/<int:id>/", cache_page(60 * 15)(ReturnLines.as_view()), name="return_data"),
    path("delete/<int:pk>/", DeleteReturn.as_view(), name="return_delete"),
    path("return-data/<int:id>/", ReturnLines.as_view(), name="return_data"),
    path("create/", ReturnCreate.as_view(), name="return_create"),
    path("batch-create/", ReturnBatchCreate.as_view(), name="return_batch_create"),
    path(
        "financial-quarters/",
        FinancialQuartersList.as_view(),
        name="financial_quarters",
    ),
    path("download-master/<int:fqid>", download_master, name="download_master"),
    path("<int:pk>/", ReturnDetail.as_view(), name="returns_detail"),
]
