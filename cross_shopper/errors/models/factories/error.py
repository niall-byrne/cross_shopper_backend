"""Factories for Error model instances."""
from __future__ import annotations

from typing import TYPE_CHECKING

import factory
from errors.models.factories.error_type import ErrorTypeFactory
from items.models.factories.item import ItemFactory
from scrapers.models.factories.scraper_config import ScraperConfigFactory
from stores.models.factories.store import StoreFactory

if TYPE_CHECKING:
  from errors.models import Error, ErrorType  # noqa: F401
  from items.models import Item
  from scrapers.models import ScraperConfig
  from stores.models import Store
  from .typing import AliasFaker, AliasSubFactory


class ErrorFactory(factory.django.DjangoModelFactory["Error"]):
  is_reoccurring: AliasFaker[bool] = factory.Faker("pybool")
  type: AliasSubFactory[ErrorType] = factory.SubFactory(ErrorTypeFactory)
  item: AliasSubFactory[Item] = factory.SubFactory(ItemFactory)
  scraper_config: AliasSubFactory[ScraperConfig] = factory.SubFactory(
      ScraperConfigFactory
  )
  store: AliasSubFactory[Store] = factory.SubFactory(StoreFactory)

  class Meta:
    model = "errors.Error"
