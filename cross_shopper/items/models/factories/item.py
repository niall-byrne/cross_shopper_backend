"""Factories for Item model instances."""

from typing import TYPE_CHECKING, Any, Dict, List

import factory
from items.models.factories.brand import BrandFactory
from items.models.factories.packaging import PackagingFactory
from items.models.factories.price_group import PriceGroupFactory

if TYPE_CHECKING:  # no cover
  from django.db import models
  from items.models import Attribute, Brand, Item, Packaging, PriceGroup
  from scrapers.models import ScraperConfig
  from .typing import AliasFaker, AliasSubFactory

  class ItemWithPriceGroup(Item):
    price_group: "models.ForeignKey[Item, PriceGroup]"  # type: ignore[assignment]


class ItemFactory(factory.django.DjangoModelFactory["Item"]):
  is_non_gmo: "AliasFaker[bool]" = factory.Faker("boolean")
  is_organic: "AliasFaker[bool]" = factory.Faker("boolean")
  name: "AliasFaker[str]" = factory.Faker("company")
  brand: "AliasSubFactory[Brand]" = factory.SubFactory(BrandFactory)
  packaging: "AliasSubFactory[Packaging]" = factory.SubFactory(PackagingFactory)
  price_group: "AliasSubFactory[PriceGroup]" = factory.SubFactory(
      PriceGroupFactory,
      is_non_gmo=factory.SelfAttribute("..is_non_gmo"),
      is_organic=factory.SelfAttribute("..is_organic"),
      unit=factory.SelfAttribute("..packaging.unit"),
  )

  class Meta:
    model = "items.Item"

  @factory.post_generation
  def attributes(  # type: ignore[misc]
      obj: "Item",
      create: bool,
      extracted: List["Attribute"],
      **kwargs: Dict[str, Any],
  ) -> None:
    """Generate Attribute instances for the created Item instance."""
    if create and extracted:
      for attribue in extracted:
        obj.attribute.add(attribue)

  @factory.post_generation
  def scraper_configs(  # type: ignore[misc]
      obj: "Item",
      create: bool,
      extracted: List["ScraperConfig"],
      **kwargs: Dict[str, Any],
  ) -> None:
    """Generate ScraperConfig instances for the created Item instance."""
    if create and extracted:
      for scraper_config in extracted:
        obj.scraper_config.add(scraper_config)
