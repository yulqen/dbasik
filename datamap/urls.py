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

urlpatterns = [
    path("datamaps/", DatamapList.as_view(), name="datamap-list"),
    path("createdatamap/", datamap_create, name="datamap-create"),
    path("datamap/<slug:slug>", datamap_detail, name="datamap-detail"),
    path("datamap/<slug:slug>/delete", datamap_delete, name="datamap-delete"),
    path("uploaddatamap/", upload_datamap, name="uploaddatamap"),
    path("edit-datamapline/<int:dml_pk>", datamapline_update, name="datamapline-update"),
    path("create-datamapline/<slug:slug>", datamapline_create, name="datamapline-create"),
]
