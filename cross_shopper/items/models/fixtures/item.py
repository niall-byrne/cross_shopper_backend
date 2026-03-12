"""Fixtures for building Item models."""

from typing import TYPE_CHECKING

import pytest
from items.models.factories.item import ItemFactory

if TYPE_CHECKING:  # no cover
  from items.models import Attribute, Item
  from scrapers.models import ScraperConfig


@pytest.fixture
def item(attribute: "Attribute", scraper_config: "ScraperConfig") -> "Item":
  return ItemFactory.create(
      attributes=[attribute],
      scraper_configs=[scraper_config],
  )


@pytest.fixture
def item_alternate(
    attribute_alternate: "Attribute",
    scraper_config_alternate: "ScraperConfig",
) -> "Item":
  return ItemFactory.create(
      attributes=[attribute_alternate],
      scraper_configs=[scraper_config_alternate],
  )
