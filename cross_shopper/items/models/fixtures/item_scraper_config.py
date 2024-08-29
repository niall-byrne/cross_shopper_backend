"""Fixtures for building Item models."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from items.models.factories.item_scraper_config import ItemScraperConfigFactory

if TYPE_CHECKING:
  from items.models import ItemScraperConfig


@pytest.fixture
def item_scraper_config() -> ItemScraperConfig:
  return ItemScraperConfigFactory.create()
