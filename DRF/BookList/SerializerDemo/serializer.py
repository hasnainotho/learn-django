from rest_framework import serializers
from .models import SerializerMenu


class SerializerMenuItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerializerMenu
        fields = ['id', 'title', 'quantity', 'description']