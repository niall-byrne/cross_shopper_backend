"""Serializer to retrieve, list, create or update PriceGroups."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db import transaction
from items.models import Attribute, PackagingUnit, PriceGroup
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from utilities.models.fields.blonde import BlondeCharField
from utilities.models.serializers.fields.slug_related_field import (
    CreatableSlugRelatedField,
)

if TYPE_CHECKING:
  from rest_framework.validators import Validator


class PriceGroupSerializerRW(serializers.ModelSerializer[PriceGroup]):
  """Serializer to retrieve, list, create or update PriceGroups."""

  name = BlondeCharField(max_length=80, blank=False)
  attribute = CreatableSlugRelatedField(
      case_sensitive=False,
      queryset=Attribute.objects.all(),
      slug_field="name",
      write_only=True,
      many=True,
      required=False,
      default=[],
  )
  unit = CreatableSlugRelatedField(
      case_sensitive=False,
      queryset=PackagingUnit.objects.all(),
      slug_field="name",
      required=False,
  )

  class Meta:
    model = PriceGroup
    fields = (
        "id",
        "name",
        "attribute",
        "is_non_gmo",
        "is_organic",
        "quantity",
        "unit",
    )

  @transaction.atomic
  def create(
      self,
      validated_data: dict[str, Any],
  ) -> PriceGroup:
    """Create a new instance."""
    attributes = validated_data.pop("attribute", [])

    price_group = PriceGroup.objects.create(**validated_data)
    price_group.attribute.set(attributes)

    return price_group

  def get_validators(self) -> list[Validator[Any]]:
    """Filter out the UniqueTogetherValidator."""
    validators = super().get_validators()
    return [
        validator for validator in validators
        if not isinstance(validator, UniqueTogetherValidator)
    ]
