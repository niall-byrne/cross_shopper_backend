"""Serializer for the PackagingUnit model."""

from items.models import PackagingUnit
from rest_framework import serializers
from utilities.models.serializers.fields.blonde import BlondeCharField


class PackagingUnitSerializer(serializers.ModelSerializer[PackagingUnit]):
  """Serializer for the PackagingUnit model."""

  name = BlondeCharField(max_length=80, allow_blank=False)

  class Meta:
    model = PackagingUnit
    fields = ('name',)
