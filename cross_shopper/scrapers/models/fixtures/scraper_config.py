"""Fixtures for building ScraperConfig models."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from scrapers.models.factories.scraper_config import ScraperConfigFactory

if TYPE_CHECKING:
  from scrapers.models import ScraperConfig


@pytest.fixture
def scraper_config() -> ScraperConfig:
  return ScraperConfigFactory.create()
