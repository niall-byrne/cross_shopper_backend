"""Serializer to retrieve, list, create or update an Item."""
from __future__ import annotations

from typing import Any

from django.db import transaction
from items.models import Attribute, Brand, Item
from items.models.packaging import Packaging
from items.models.price_group import PriceGroup
from items.models.serializers.read_write.packaging import PackagingSerializerRW
from items.models.serializers.read_write.price_group import (
    PriceGroupSerializerRW,
)
from items.models.validators.item import model_level_validators
from rest_framework import serializers
from scrapers.models import ScraperConfig
from scrapers.models.serializers.read_only.scraper_config import (
    ScraperConfigSerializerRO,
)
from utilities.models.serializers.fields.blonde import BlondeCharField
from utilities.models.serializers.fields.slug_related_field import (
    CreatableSlugRelatedField,
)


class ItemSerializerRW(serializers.ModelSerializer[Item]):
  """Serializer to retrieve, list, create or update an Item."""

  name = BlondeCharField(max_length=80, allow_blank=False)
  name_full = serializers.CharField(read_only=True)
  attribute = CreatableSlugRelatedField(
      case_sensitive=False,
      queryset=Attribute.objects.all(),
      slug_field="name",
      write_only=True,
      many=True,
  )
  brand = CreatableSlugRelatedField(
      case_sensitive=False,
      queryset=Brand.objects.all(),
      slug_field="name",
  )
  packaging = PackagingSerializerRW()
  price_group = PriceGroupSerializerRW()
  is_bulk = serializers.BooleanField(read_only=True)
  scraper_config = ScraperConfigSerializerRO(many=True)

  def to_internal_value(self, data: dict[str, Any]) -> Any:
    """Append derived values to the price_group serializer data."""
    price_group_data = data.get("price_group")
    packaging_data = data.get("packaging", {})

    if isinstance(price_group_data, dict):
      price_group_data.setdefault("is_non_gmo", data.get("is_non_gmo"))
      price_group_data.setdefault("is_organic", data.get("is_organic"))
      price_group_data.setdefault("unit", packaging_data.get("unit"))

    return super().to_internal_value(data)

  class Meta:
    model = Item
    fields = (
        "id",
        "attribute",
        "name",
        "name_full",
        "brand",
        "packaging",
        "price_group",
        "is_bulk",
        "is_non_gmo",
        "is_organic",
        "scraper_config",
    )

  @transaction.atomic
  def create(self, validated_data: dict[str, Any]) -> Item:
    """Create a new instance."""
    attributes = validated_data.pop("attribute", [])

    packaging_data = validated_data.pop("packaging")
    packaging = Packaging.objects.get_or_create(**packaging_data)[0]

    price_group_data = validated_data.pop("price_group")
    price_group_attributes = price_group_data.pop("attribute", [])
    price_group = PriceGroup.objects.get_or_create(**price_group_data)[0]
    price_group.attribute.add(*price_group_attributes)

    scraper_configs_data = validated_data.pop("scraper_config", [])
    scraper_configs = [
        ScraperConfig.objects.get_or_create(**scraper_config)[0]
        for scraper_config in scraper_configs_data
    ]

    item = Item.objects.create(
        **validated_data,
        packaging=packaging,
        price_group=price_group,
    )

    item.attribute.set(attributes)
    item.scraper_config.set(scraper_configs)

    return item

  def validate(self, attrs: dict[str, Any]) -> Any:
    """Perform model level validation."""
    for validator in model_level_validators:
      if not validator.is_serializer_valid(attrs):
        raise validator.generate_serializer_error()

    return super().validate(attrs)
