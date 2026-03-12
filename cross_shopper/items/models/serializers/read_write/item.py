"""Serializer to retrieve, list, create or update an Item."""

from typing import Any, Dict, Sequence, cast

from items.models import Attribute, Brand, Item
from items.models.serializers.read_write.packaging import PackagingSerializerRW
from items.models.serializers.read_write.price_group import (
    PriceGroupSerializerRW,
)
from rest_framework import serializers
from scrapers.models.scraper_config import ScraperConfig
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
      slug_field='name',
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

  class Meta:
    model = Item
    fields = (
        'id',
        'attribute',
        'name',
        'name_full',
        'brand',
        'packaging',
        'price_group',
        'is_bulk',
        'is_non_gmo',
        'is_organic',
        'scraper_config',
    )

  def create(self, validated_data: Dict[str, Any]) -> Item:
    """Create a new instance."""
    attribute = validated_data.pop('attribute')

    packaging = cast(
        PackagingSerializerRW,
        self.fields['packaging'],
    ).create(validated_data.pop('packaging'))

    price_group = cast(
        PriceGroupSerializerRW,
        self.fields['price_group'],
    ).create(validated_data.pop('price_group'))

    scraper_config = cast(
        Sequence[ScraperConfig],
        cast(
            ScraperConfigSerializerRO,
            self.fields['scraper_config'],
        ).create(validated_data.pop("scraper_config"))
    )

    item = Item.objects.create(
        **validated_data,
        packaging=packaging,
        price_group=price_group,
    )
    item.attribute.set(attribute)
    item.scraper_config.set(scraper_config)
    return item
