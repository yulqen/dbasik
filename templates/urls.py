from django.urls import path

from .views import (
    template_create,
    TemplateList,
    TemplateDetail,
    TemplateUpdate,
    TemplateDelete,
)
from excelparser.views import ProcessPopulatedTemplate

app_name = "templates"

urlpatterns = [
    path("", TemplateList.as_view(), name="list"),
    path("create/", template_create, name="create"),
    path("update/<slug:slug>", TemplateUpdate.as_view(), name="update"),
    path("delete/<slug:slug>/", TemplateDelete.as_view(), name="delete"),
    path("<slug:slug>/", TemplateDetail.as_view(), name="template_detail"),
]
