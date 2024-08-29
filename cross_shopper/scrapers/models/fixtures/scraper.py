"""Fixtures for building Scraper models."""

from typing import TYPE_CHECKING

import pytest
from scrapers.models.factories.scraper import ScraperFactory

if TYPE_CHECKING:  # no cover
  from scrapers.models import Scraper


@pytest.fixture
def scraper() -> "Scraper":
  return ScraperFactory.create()
