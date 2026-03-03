"""Serializer to retrieve, list, create or update a Brand."""

from items.models import Brand
from rest_framework import serializers
from utilities.models.serializers.fields.blonde import BlondeCharField


class BrandSerializerRW(serializers.ModelSerializer):
  """Serializer to retrieve, list, create or update a Brand."""

  name = BlondeCharField(max_length=80, allow_blank=False)

  class Meta:
    model = Brand
    fields = ('name',)
