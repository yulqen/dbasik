from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    template_create,
    TemplateList,
    TemplateDetail,
    TemplateUpdate,
    TemplateDelete,
)
app_name = "templates"

urlpatterns = [
    path("", TemplateList.as_view(), name="list"),
    path("create/", template_create, name="create"),
    path("update/<slug:slug>", TemplateUpdate.as_view(), name="update"),
    path("delete/<slug:slug>/", TemplateDelete.as_view(), name="delete"),
    path("<slug:slug>/", TemplateDetail.as_view(), name="template_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
