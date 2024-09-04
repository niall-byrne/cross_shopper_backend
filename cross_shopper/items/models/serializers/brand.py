"""Serializer for the Brand model."""

from items.models import Brand
from rest_framework import serializers
from utilities.models.serializers.fields.blonde import BlondeCharField


class BrandSerializer(serializers.ModelSerializer[Brand]):
  """Serializer for the Brand model."""

  name = BlondeCharField(max_length=80, allow_blank=False)

  class Meta:
    model = Brand
    fields = ("name",)
