from django.urls import path
from .views import (
    DatamapList,
    create_datamap,
    datamap_view,
    upload_datamap,
    delete_datamap_view,
    edit_datamapline
)

urlpatterns = [
    path("datamaps/", DatamapList.as_view(), name="datamaps"),
    path("createdatamap/", create_datamap, name="createdatamap"),
    path("datamap/<int:dm_pk>", datamap_view, name="datamap"),
    path("datamap/<int:dm_pk>/delete", delete_datamap_view, name="delete-datamap"),
    path("uploaddatamap/", upload_datamap, name="uploaddatamap"),
    path("edit-datamapline/<int:dml_pk>", edit_datamapline, name="edit-datamapline"),
]
