"""Serializer to retrieve, list, create or update an Item."""

from typing import TYPE_CHECKING, Any, Sequence, cast

from items.models import Brand, Item
from items.models.serializers.read_write.packaging import PackagingSerializerRW
from rest_framework import serializers
from scrapers.models.serializers.read_only.scraper_config import (
    ScraperConfigSerializerRO,
)
from utilities.models.serializers.fields.blonde import BlondeCharField

if TYPE_CHECKING:
  from scrapers.models.scraper_config import ScraperConfig


class ItemSerializerRW(serializers.ModelSerializer[Item]):
  """Serializer to retrieve, list, create or update an Item."""

  name = BlondeCharField(max_length=80, allow_blank=False)
  full_name = serializers.CharField(read_only=True)
  brand = BlondeCharField(
      max_length=80,
      allow_blank=False,
      source="brand.name",
  )
  packaging = PackagingSerializerRW()
  is_bulk = serializers.BooleanField(read_only=True)
  scraper_config = ScraperConfigSerializerRO(many=True)

  class Meta:
    model = Item
    fields = (
        "id",
        "name",
        "full_name",
        "brand",
        "packaging",
        "is_bulk",
        "is_non_gmo",
        "is_organic",
        "scraper_config",
    )

  def create(self, validated_data: dict[str, Any]) -> Item:
    """Create a new instance."""
    brand = Brand.objects.get_or_create(**validated_data.pop("brand"))[0]

    packaging = cast(
        "PackagingSerializerRW",
        self.fields["packaging"],
    ).create(validated_data.pop("packaging"))

    scraper_config = cast(
        "Sequence[ScraperConfig]",
        cast(
            "ScraperConfigSerializerRO",
            self.fields["scraper_config"],
        ).create(validated_data.pop("scraper_config"))
    )

    item = Item.objects.create(
        **validated_data,
        brand=brand,
        packaging=packaging,
    )
    item.scraper_config.set(scraper_config)
    return item
