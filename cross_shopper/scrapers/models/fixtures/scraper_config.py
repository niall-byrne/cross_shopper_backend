"""Fixtures for building ScraperConfig models."""

from typing import TYPE_CHECKING

import pytest
from scrapers.models.factories.scraper_config import ScraperConfigFactory

if TYPE_CHECKING:  # no cover
  from scrapers.models import ScraperConfig


@pytest.fixture
def scraper_config() -> "ScraperConfig":
  return ScraperConfigFactory.create()
