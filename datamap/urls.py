from django.urls import path
from . views import DatamapList, create_datamap

urlpatterns = [
    path('datamaps/', DatamapList.as_view(), name='datamaps'),
    path('createdatamap/', create_datamap, name='createdatamap'),
]
