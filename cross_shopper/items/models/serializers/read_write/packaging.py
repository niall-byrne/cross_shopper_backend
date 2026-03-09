"""Serializer to retrieve, list, create or update Packaging."""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any

from items.models import Packaging, PackagingContainer, PackagingUnit
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from utilities.models.serializers.fields.slug_related_field import (
    CreatableSlugRelatedField,
)

if TYPE_CHECKING:
  from rest_framework.validators import Validator


class PackagingSerializerRW(serializers.ModelSerializer[Packaging]):
  """Serializer to retrieve, list, create or update Packaging."""

  ERROR_MESSAGE_QUANTITY_IS_NULL = (
      "This field cannot be null if a container is specified."
  )
  ERROR_MESSAGE_CONTAINER_IS_NULL = (
      "This field cannot be null if a quantity is specified."
  )

  quantity = serializers.DecimalField(
      min_value=Decimal(1),
      allow_null=True,
      max_digits=11,
      decimal_places=2,
  )
  unit = CreatableSlugRelatedField(
      case_sensitive=False,
      queryset=PackagingUnit.objects.all(),
      slug_field="name",
  )
  container = CreatableSlugRelatedField(
      allow_null=True,
      case_sensitive=False,
      queryset=PackagingContainer.objects.all(),
      slug_field="name",
  )

  class Meta:
    model = Packaging
    fields = ("quantity", "unit", "container")
    read_only = fields

  def create(
      self,
      validated_data: dict[str, Any],
  ) -> Packaging:
    """Create a new instance."""
    return Packaging.objects.get_or_create(**validated_data,)[0]

  def get_validators(self) -> list[Validator[Any]]:
    """Filter out the UniqueTogetherValidator."""
    validators = super().get_validators()
    return [
        validator for validator in validators
        if not isinstance(validator, UniqueTogetherValidator)
    ]

  def validate_quantity(self, value: int | None) -> int | None:
    """Perform quantity field validation."""
    if value is None and self.initial_data["container"] is not None:
      raise ValidationError(self.ERROR_MESSAGE_QUANTITY_IS_NULL)
    return value

  def validate_container(self, value: str | None) -> str | None:
    """Perform container field validation."""
    if value is None and self.initial_data["quantity"] is not None:
      raise ValidationError(self.ERROR_MESSAGE_CONTAINER_IS_NULL)
    return value
