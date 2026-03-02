"""Serializer for the Error model."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from errors.models import Error, ErrorType
from rest_framework import serializers

if TYPE_CHECKING:
  from rest_framework import validators


class ErrorSerializerRW(serializers.ModelSerializer[Error]):
  """Serializer for creating or updating an Error model instance."""

  type = serializers.SlugRelatedField(
      queryset=ErrorType.objects.all(),
      slug_field="name",
  )

  class Meta:
    model = Error
    fields = (
        "id",
        "type",
        "item",
        "is_reoccurring",
        "scraper_config",
        "store",
    )

  def get_unique_together_validators(
      self,
  ) -> list[validators.UniqueTogetherValidator]:
    """Disable unique together checks to enable upsert operations."""
    return []

  def create(
      self,
      validated_data: dict[str, Any],
  ) -> Error:
    """Create or update an Error instance."""
    instance, created = Error.objects.update_or_create(**validated_data)
    self.context["created"] = created

    if not created:
      instance.count += 1
      instance.save()

    return instance
