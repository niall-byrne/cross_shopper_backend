"""Serializer to retrieve, list, create or update PriceGroups."""

from functools import lru_cache
from typing import TYPE_CHECKING

from django.core.exceptions import ObjectDoesNotExist
from items.models import PackagingUnit, PriceGroup
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail, ValidationError
from utilities.models.fields.blonde import BlondeCharField
from utilities.models.serializers.fields.slug_related_field import (
    CreatableSlugRelatedField,
)

if TYPE_CHECKING:  # no cover
  from typing import Any, Dict, Optional


class PriceGroupSerializerRW(serializers.ModelSerializer[PriceGroup]):
  """Serializer to retrieve, list, create or update PriceGroups."""

  name = BlondeCharField(max_length=80, blank=False)
  unit = CreatableSlugRelatedField(
      case_sensitive=False,
      queryset=PackagingUnit.objects.all(),
      slug_field="name",
      required=False,
  )

  class Meta:
    model = PriceGroup
    fields = ('name', 'quantity', 'unit')
    extra_kwargs = {'quantity': {'required': False}}

  @lru_cache(maxsize=1)
  def existing_price_group(self, name: str) -> "Optional[PriceGroup]":
    """Return any existing price group matching the given name."""
    try:
      return PriceGroup.objects.get(name=name)
    except ObjectDoesNotExist:
      return None

  def create(
      self,
      validated_data: "Dict[str, Any]",
  ) -> PriceGroup:
    """Create a new instance."""
    existing_price_group = self.existing_price_group(validated_data['name'])
    if existing_price_group:
      return existing_price_group
    return PriceGroup.objects.create(**validated_data)

  def validate(self, attrs: "Dict[str, Any]") -> "Any":
    """Perform model level validation accross all serializer fields."""
    if not self.existing_price_group(attrs.get('name', None)):
      for field_name in ('quantity', 'unit'):
        if field_name not in attrs:
          raise ValidationError(
              {
                  field_name:
                      [
                          ErrorDetail(
                              string=str(
                                  serializers.Field.
                                  default_error_messages['required']
                              ),
                              code='required'
                          )
                      ]
              }
          )

    return super().validate(attrs)
