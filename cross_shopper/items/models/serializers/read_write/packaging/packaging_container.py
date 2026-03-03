"""Serializer to retrieve, list, create or update a PackagingContainer."""

from items.models import PackagingContainer
from rest_framework import serializers
from utilities.models.serializers.fields.title import TitleField


class PackagingContainerSerializerRW(
    serializers.ModelSerializer[PackagingContainer],
):
  """Serializer to retrieve, list, create or update a PackagingContainer."""

  name = TitleField(max_length=80, allow_blank=False)

  class Meta:
    model = PackagingContainer
    fields = ("name",)
