from django.urls import path
from .views import (
    DatamapCreate,
    DatamapList,
    DatamapUpdate,
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
    path("create/", DatamapCreate.as_view(), name="datamap-create"),
    path("update/<slug:slug>", DatamapUpdate.as_view(), name="datamap_update"),
    path("delete/<slug:slug>/", datamap_delete, name="delete"),
    path("edit-datamapline/<int:dml_pk>/", datamapline_update, name="datamapline-update"),
    path("create-datamapline/<slug:slug>/", datamapline_create, name="datamapline-create"),
    path("<slug:slug>/", datamap_detail, name="datamap-detail"),
    path("uploaddatamap/", upload_datamap, name="uploaddatamap"),
]
