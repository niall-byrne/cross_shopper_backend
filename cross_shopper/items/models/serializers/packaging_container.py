"""Serializer for the PackagingContainer model."""

from items.models import PackagingContainer
from rest_framework import serializers
from utilities.models.serializers.fields.title import TitleField


class PackagingContainerSerializer(
    serializers.ModelSerializer[PackagingContainer],
):
  """Serializer for the PackagingContainer model."""

  name = TitleField(max_length=80, allow_blank=False)

  class Meta:
    model = PackagingContainer
    fields = ('name',)
