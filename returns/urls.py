from django.urls import path

from . views import ReturnsList

app_name = "returns"

urlpatterns = [
    path("", ReturnsList.as_view(), name="returns_list"),
]