from django.urls import path

from .views import (
    ProjectCreate,
    ProjectDelete,
    ProjectDetail,
    ProjectList,
    ProjectStageCreate,
    ProjectStageDelete,
    ProjectStageDetail,
    ProjectStageList,
    ProjectStageUpdate,
    ProjectTypeCreate,
    ProjectTypeDelete,
    ProjectTypeDetail,
    ProjectTypeList,
    ProjectTypeUpdate,
    ProjectUpdate,
    StrategicAlignmentCreate,
    StrategicAlignmentDelete,
    StrategicAlignmentDetail,
    StrategicAlignmentList,
    StrategicAlignmentUpdate,
    TierCreate,
    TierDelete,
    TierDetail,
    TierList,
    TierUpdate,
)

app_name = "register"

urlpatterns = [
    path(
        "projecttype/<slug:slug>/update",
        ProjectTypeUpdate.as_view(),
        name="projecttype_update",
    ),
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
    path(
        "projectstage/<slug:slug>/update",
        ProjectStageUpdate.as_view(),
        name="projectstage_update",
    ),
    path(
        "projectstage/create", ProjectStageCreate.as_view(), name="projectstage_create"
    ),
    path(
        "projectstage/<slug:slug>",
        ProjectStageDetail.as_view(),
        name="projectstage_detail",
    ),
    path("projectstage/", ProjectStageList.as_view(), name="projectstage_list"),
    path(
        "projectstage/<slug:slug>/delete",
        ProjectStageDelete.as_view(),
        name="projectstage_delete",
    ),
    path(
        "strategicalignment/<slug:slug>/update",
        StrategicAlignmentUpdate.as_view(),
        name="strategicalignment_update",
    ),
    path(
        "strategicalignment/create",
        StrategicAlignmentCreate.as_view(),
        name="strategicalignment_create",
    ),
    path(
        "strategicalignment/<slug:slug>",
        StrategicAlignmentDetail.as_view(),
        name="strategicalignment_detail",
    ),
    path(
        "strategicalignment/",
        StrategicAlignmentList.as_view(),
        name="strategicalignment_list",
    ),
    path(
        "strategicalignment/<slug:slug>/delete",
        StrategicAlignmentDelete.as_view(),
        name="strategicalignment_delete",
    ),
    path("project/<slug:slug>/update", ProjectUpdate.as_view(), name="project_update"),
    path("project/create", ProjectCreate.as_view(), name="project_create"),
    path(
        "project/<slug:slug>",
        ProjectDetail.as_view(),
        name="project-detail",
    ),
    path("project/", ProjectList.as_view(), name="project_list"),
    path(
        "project/<slug:slug>/delete",
        ProjectDelete.as_view(),
        name="project_delete",
    ),
]
