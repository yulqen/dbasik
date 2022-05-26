from register.models import Tier, Project
from rest_framework import serializers

class TierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tier
        fields = ['name', 'slug', 'description']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'slug', 'tier']

