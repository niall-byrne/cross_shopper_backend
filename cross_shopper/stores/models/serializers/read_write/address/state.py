"""Serializer to retrieve, list, create or update States."""

from address.models import State
from rest_framework import serializers
from .country import CountrySerializer


class StateSerializer(serializers.ModelSerializer[State]):
  """Serializer to retrieve, list, create or update States."""

  country = CountrySerializer()

  class Meta:
    model = State
    fields = "__all__"
