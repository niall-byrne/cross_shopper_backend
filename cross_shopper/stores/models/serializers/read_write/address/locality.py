"""Serializer to retrieve, list, create or update Localities."""

from address.models import Locality
from rest_framework import serializers
from .state import StateSerializer


class LocalitySerializer(serializers.ModelSerializer):
  """Serializer to retrieve, list, create or update Localities."""

  state = StateSerializer()

  class Meta:
    model = Locality
    fields = '__all__'
