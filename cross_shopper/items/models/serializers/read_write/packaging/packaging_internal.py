"""Serializer for internal representations of Packaging model instance."""

from items.models import Packaging
from rest_framework import serializers
from .packaging_container import PackagingContainerSerializerRW
from .packaging_unit import PackagingUnitSerializerRW


class PackagingSerializerInternal(serializers.ModelSerializer[Packaging]):

  container = PackagingContainerSerializerRW()
  unit = PackagingUnitSerializerRW()

  class Meta:
    model = Packaging
    fields = ("quantity", "unit", "container")
