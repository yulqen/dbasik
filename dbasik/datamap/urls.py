from django.urls import path
from .views import (
    DatamapCreate,
    DatamapList,
    DatamapUpdate,
    DatamapDelete,
    datamap_detail,
    DatamapLineCreate,
    DatamapLineUpdate,
    DatamapLineDelete,
    UploadDatamapView,
)

app_name = "datamaps"

urlpatterns = [
    path("", DatamapList.as_view(), name="datamap_list"),
    path("create/", DatamapCreate.as_view(), name="datamap-create"),
    path("update/<slug:slug>", DatamapUpdate.as_view(), name="datamap_update"),
    path("delete/<slug:slug>/", DatamapDelete.as_view(), name="datamap_delete"),
    path(
        "datamapline/<int:pk>/update",
        DatamapLineUpdate.as_view(),
        name="datamapline_update",
    ),
    path(
        "datamapline/<int:pk>/delete",
        DatamapLineDelete.as_view(),
        name="datamapline_delete",
    ),
    path(
        "uploaddatamap/<slug:slug>/", UploadDatamapView.as_view(), name="uploaddatamap"
    ),
    path(
        "create-datamapline/<slug:slug>",
        DatamapLineCreate.as_view(),
        name="datamapline-create",
    ),
    path("<slug:slug>/", datamap_detail, name="datamap_detail"),
]
