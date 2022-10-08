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
from dbasik.datamap import views as dmviews
from dbasik.register import views as regviews
from dbasik.returns import views as retviews
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("dbasik.core.urls")),
    path("datamaps/", include("dbasik.datamap.urls", namespace="datamaps")),
    path("register/", include("dbasik.register.urls", namespace="register")),
    path("templates/", include("dbasik.templates.urls", namespace="templates")),
    path("excelparser/", include("dbasik.excelparser.urls", namespace="excelparser")),
    path("returns/", include("dbasik.returns.urls", namespace="returns")),
]
