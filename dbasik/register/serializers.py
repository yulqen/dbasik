from rest_framework import serializers

from register.models import FinancialQuarter, Project, Tier


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
            "abbreviation",
            "dft_group",
            "gmpp",
        ]


class FinancialQuarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialQuarter
        fields = ["quarter", "year", "start_date", "end_date", "label"]
