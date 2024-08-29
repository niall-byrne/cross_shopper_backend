"""Fixtures for building Scraper models."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from scrapers.models.factories.scraper import ScraperFactory

if TYPE_CHECKING:
  from scrapers.models import Scraper


@pytest.fixture
def scraper() -> Scraper:
  return ScraperFactory.create()
