"""Factories for Item model instances."""

from typing import TYPE_CHECKING, Any, Dict, List

import factory
from items.models.factories.brand import BrandFactory
from items.models.factories.packaging import PackagingFactory
from scrapers.models.factories.scraper_config import ScraperConfigFactory

if TYPE_CHECKING:  # no cover
  from items.models import (  # noqa: F401
    Brand,
    Item,
    ItemScraperConfig,
    Packaging,
  )
  from scrapers.models import ScraperConfig
  from .typing import AliasFaker, AliasSubFactory


class ItemFactory(factory.django.DjangoModelFactory["Item"]):
  is_non_gmo: "AliasFaker[bool]" = factory.Faker('boolean')
  is_organic: "AliasFaker[bool]" = factory.Faker('boolean')
  name: "AliasFaker[str]" = factory.Faker('company')
  brand: "AliasSubFactory[Brand]" = factory.SubFactory(BrandFactory)
  packaging: "AliasSubFactory[Packaging]" = factory.SubFactory(PackagingFactory)

  class Meta:
    model = 'items.Item'

  @factory.post_generation
  def scraper_configs(
      self,
      create: bool,
      extracted: List["ScraperConfig"],
      **kwargs: Dict[str, Any],
  ) -> None:
    """Generate ScraperConfig instances for the created Item instance."""
    if create and extracted:
      for scraper_config in extracted:
        self.scraper_config.add(scraper_config)  # type: ignore[attr-defined]


class ItemScraperConfigFactory(
    factory.django.DjangoModelFactory["ItemScraperConfig"]
):
  item: "AliasSubFactory[Item]" = factory.SubFactory(ItemFactory)
  scraper_config: "AliasSubFactory[ScraperConfig]" = factory.SubFactory(
      ScraperConfigFactory
  )

  class Meta:
    model = 'items.ItemScraperConfig'
