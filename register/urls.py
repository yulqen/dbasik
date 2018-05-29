from django.urls import path
from .views import (
    ProjectTypeCreate,
    ProjectTypeList,
    ProjectTypeDetail,
    ProjectTypeDelete,
)

app_name = "register"

urlpatterns = [
    path("projecttype/create", ProjectTypeCreate.as_view(), name="projecttype_create"),
    path(
        "projecttype/<slug:slug>",
        ProjectTypeDetail.as_view(),
        name="projecttype_detail",
    ),
    path("projecttype/", ProjectTypeList.as_view(), name="projecttype_list"),
    path(
        "projecttype/<slug:slug>/delete",
        ProjectTypeDelete.as_view(),
        name="projecttype_delete",
    ),
]
