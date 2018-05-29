from django.urls import path
from .views import (
    DatamapList,
    datamap_create,
    datamap_detail,
    upload_datamap,
    datamap_delete,
    datamapline_update,
    datamapline_create,
)

app_name = "datamaps"

urlpatterns = [
    path("", DatamapList.as_view(), name="datamap-list"),
    path("create/", datamap_create, name="datamap-create"),
    path("uploaddatamap/", upload_datamap, name="uploaddatamap"),
    path("delete/<slug:slug>/", datamap_delete, name="datamap-delete"),
    path("edit-datamapline/<int:dml_pk>/", datamapline_update, name="datamapline-update"),
    path("create-datamapline/<slug:slug>/", datamapline_create, name="datamapline-create"),
    path("<slug:slug>/", datamap_detail, name="datamap-detail"),
]
