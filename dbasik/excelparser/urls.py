from django.urls import path

from .views import (
    ProcessPopulatedTemplate,
)

app_name = "excelparser"

urlpatterns = [
    path(
        "process-populated/<int:return_id>/",
        ProcessPopulatedTemplate.as_view(),
        name="process_populated",
    ),
]
