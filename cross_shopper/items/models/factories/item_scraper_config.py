"""Factories for ItemScraperConfig model instances."""
from __future__ import annotations

from typing import TYPE_CHECKING

import factory
from items.models.factories.item import ItemFactory
from scrapers.models.factories.scraper_config import ScraperConfigFactory

if TYPE_CHECKING:
  from items.models import Item, ItemScraperConfig  # noqa: F401
  from scrapers.models import ScraperConfig
  from .typing import AliasSubFactory


class ItemScraperConfigFactory(
    factory.django.DjangoModelFactory["ItemScraperConfig"],
):
  item: AliasSubFactory[Item] = factory.SubFactory(ItemFactory)
  scraper_config: AliasSubFactory[ScraperConfig] = factory.SubFactory(
      ScraperConfigFactory
  )

  class Meta:
    model = "items.ItemScraperConfig"
