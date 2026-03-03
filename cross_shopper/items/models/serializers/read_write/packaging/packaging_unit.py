"""Serializer to retrieve, list, create or update a PackagingUnit."""

from items.models import PackagingUnit
from rest_framework import serializers
from utilities.models.serializers.fields.blonde import BlondeCharField


class PackagingUnitSerializerRW(
    serializers.ModelSerializer[PackagingUnit],
):
  """Serializer to retrieve, list, create or update a PackagingUnit."""

  name = BlondeCharField(max_length=80, allow_blank=False)

  class Meta:
    model = PackagingUnit
    fields = ('name',)
