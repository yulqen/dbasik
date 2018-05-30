from django.urls import path
from .views import (
    ProjectTypeCreate,
    ProjectTypeList,
    ProjectTypeDetail,
    ProjectTypeDelete,
    ProjectTypeUpdate,
    TierCreate,
    TierList,
    TierDetail,
    TierDelete,
    TierUpdate
)

app_name = "register"

urlpatterns = [
    path("projecttype/<slug:slug>/update", ProjectTypeUpdate.as_view(), name="projecttype_update"),
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

    path("tier/<slug:slug>/update", TierUpdate.as_view(), name="tier_update"),
    path("tier/create", TierCreate.as_view(), name="tier_create"),
    path(
        "tier/<slug:slug>",
        TierDetail.as_view(),
        name="tier_detail",
    ),
    path("tier/", TierList.as_view(), name="tier_list"),
    path(
        "tier/<slug:slug>/delete",
        TierDelete.as_view(),
        name="tier_delete",
    ),
]
