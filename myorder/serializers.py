from rest_framework import serializers
from myorder.models import Items


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['name', 'unit']