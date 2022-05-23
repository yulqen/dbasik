from rest_framework import serializers

from returns.models import Return, ReturnItem


class ReturnSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Return
        fields = ["project", "financial_quarter"]


class ReturnItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReturnItem
        fields = [
            "parent",
            "datamapline",
            "value_str",
            "value_int",
            "value_float",
            "value_date",
            "value_datetime",
            "value_phone",
        ]
