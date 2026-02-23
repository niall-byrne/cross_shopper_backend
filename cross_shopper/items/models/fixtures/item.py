"""Fixtures for building Item models."""

from typing import TYPE_CHECKING

import pytest
from items.models.factories.item import ItemFactory

if TYPE_CHECKING:  # no cover
  from items.models import Item
  from scrapers.models import ScraperConfig


@pytest.fixture
def item(scraper_config: "ScraperConfig") -> "Item":
  return ItemFactory.create(scraper_configs=[scraper_config])
