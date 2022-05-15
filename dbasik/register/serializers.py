from register.models import Tier
from rest_framework import serializers

class TierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tier
        fields = ['name', 'slug', 'description']
