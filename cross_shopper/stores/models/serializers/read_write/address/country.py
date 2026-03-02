"""Serializer to retrieve, list, create or update Countries."""

from address.models import Country
from rest_framework import serializers


class CountrySerializer(serializers.ModelSerializer[Country]):
  """Serializer to retrieve, list, create or update Countries."""

  class Meta:
    model = Country
    fields = "__all__"
