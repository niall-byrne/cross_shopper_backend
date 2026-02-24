"""Serializer for the Store model in JSON format."""

from rest_framework import serializers
from stores.models import Store


class StoreJsonSerializer(serializers.ModelSerializer):
  """Serializer for the Store model in JSON format."""

  franchise_name = serializers.CharField(source='franchise.name')

  class Meta:
    model = Store
    fields = ('id', 'franchise_name')
