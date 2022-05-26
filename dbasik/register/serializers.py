from register.models import Tier, Project, FinancialQuarter
from rest_framework import serializers


class TierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tier
        fields = ["name", "slug", "description"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "slug",
            "tier",
            "project_type",
            "stage",
            "start_date",
            "planned_end_date",
            "baseline_wlc",
        ]


class FinancialQuarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialQuarter
        fields = ["quarter", "year", "start_date", "end_date", "label"]
