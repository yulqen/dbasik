"""dbasik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from datamap import views as dmviews
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from register import views as regviews
from rest_framework import routers, serializers, viewsets
from returns import views as retviews

# API routes
router = routers.DefaultRouter()
router.register(r"datamaps", dmviews.DatamapViewSet)
router.register(r"datamaplines", dmviews.DatamapLineViewSet)
router.register(r"tiers", regviews.TierViewSet)
router.register(r"returns", retviews.ReturnViewSet)
router.register(r"projects", regviews.ProjectViewSet)
router.register(r"financialquarters", regviews.FinancialQuarterViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("core.urls")),
    path("datamaps/", include("datamap.urls", namespace="datamaps")),
    path("register/", include("register.urls", namespace="register")),
    path("templates/", include("templates.urls", namespace="templates")),
    path("excelparser/", include("excelparser.urls", namespace="excelparser")),
    path("returns/", include("returns.urls", namespace="returns")),
]
