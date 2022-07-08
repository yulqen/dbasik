from rest_framework import serializers

from dbasik.returns.models import Return, ReturnItem


class ReturnSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Return
        fields = ["id", "project", "financial_quarter"]


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
