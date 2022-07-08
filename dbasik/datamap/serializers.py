from dbasik.datamap.models import Datamap, DatamapLine
from rest_framework import serializers

class DatamapLineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DatamapLine
        fields = ['datamap', 'key', 'data_type', 'required', 'max_length', 'sheet', 'cell_ref']

class DatamapSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Datamap
        fields = ['name', 'tier', 'active', 'slug']

