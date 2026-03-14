"""Fixtures for building ScraperConfig models."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from scrapers.models import ScraperConfig
from scrapers.models.factories.scraper_config import ScraperConfigFactory

if TYPE_CHECKING:
  from django.db.models import QuerySet


@pytest.fixture
def scraper_config() -> ScraperConfig:
  return ScraperConfigFactory.create()


@pytest.fixture
def scraper_config_alternate() -> ScraperConfig:
  return ScraperConfigFactory.create()


@pytest.fixture
def scraper_config_batch() -> QuerySet[ScraperConfig]:
  scraper_configs = ScraperConfigFactory.create_batch(size=10)
  return ScraperConfig.objects.filter(
      id__in=[instance.pk for instance in scraper_configs]
  )
