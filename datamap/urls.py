from django.urls import path
from .views import (
    DatamapCreate,
    DatamapList,
    DatamapUpdate,
    DatamapDelete,
    datamap_detail,
    upload_datamap,
    datamapline_update,
    DatamapLineCreate,
)

app_name = "datamaps"

urlpatterns = [
    path("", DatamapList.as_view(), name="datamap_list"),
    path("create/", DatamapCreate.as_view(), name="datamap-create"),
    path("update/<slug:slug>", DatamapUpdate.as_view(), name="datamap_update"),
    path("delete/<slug:slug>/", DatamapDelete.as_view(), name="datamap_delete"),
    path("edit-datamapline/<int:dml_pk>/", datamapline_update, name="datamapline-update"),
    path("create-datamapline/<slug:slug>", DatamapLineCreate.as_view(), name="datamapline-create"),
    path("uploaddatamap/", upload_datamap, name="uploaddatamap"),
    path("<slug:slug>/", datamap_detail, name="datamap_detail"),
]
