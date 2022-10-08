from dbasik.config.api import api
from django.contrib.auth.views import logout_then_login
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout-then-login/", logout_then_login, name="logout-the-login"),
    path("profile/", views.profile, name="profile"),
    path("api/", api.urls),
]
