from django.urls import path
from .views import (
    DatamapList,
    create_datamap,
    datamap_view,
    upload_datamap,
    delete_datamap_view,
    edit_datamapline,
    create_datamapline,
)

urlpatterns = [
    path("datamaps/", DatamapList.as_view(), name="datamaps"),
    path("createdatamap/", create_datamap, name="createdatamap"),
    path("datamap/<slug:slug>", datamap_view, name="datamap"),
    path("datamap/<slug:slug>/delete", delete_datamap_view, name="delete-datamap"),
    path("uploaddatamap/", upload_datamap, name="uploaddatamap"),
    path("edit-datamapline/<int:dml_pk>", edit_datamapline, name="edit-datamapline"),
    path("create-datamapline/<slug:slug>", create_datamapline, name="add-dmline"),
]
