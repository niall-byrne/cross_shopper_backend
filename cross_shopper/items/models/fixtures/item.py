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
