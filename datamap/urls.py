from django.urls import path
from . views import DatamapList

urlpatterns = [
    path('datamaps/', DatamapList.as_view(), name='datamaps'),
]
