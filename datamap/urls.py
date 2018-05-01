from django.urls import path
from . views import (DatamapList, create_datamap, datamap_view,
                     upload_datamap)

urlpatterns = [
    path('datamaps/', DatamapList.as_view(), name='datamaps'),
    path('createdatamap/', create_datamap, name='createdatamap'),
    path('datamap/<int:dm_pk>', datamap_view, name='datamap'),
    path('uploaddatamap/', upload_datamap, name='uploaddatamap'),
]
