"""Fixtures for building ItemScraperConfig models."""

from typing import TYPE_CHECKING

import pytest
from items.models import ItemScraperConfig
from items.models.factories.item import ItemScraperConfigFactory

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet


@pytest.fixture
def item_scraper_config() -> "ItemScraperConfig":
  return ItemScraperConfigFactory.create()


@pytest.fixture
def item_scraper_config_batch() -> "QuerySet[ItemScraperConfig]":
  item_scraper_configs = ItemScraperConfigFactory.create_batch(size=10)
  return ItemScraperConfig.objects.filter(
      id__in=[instance.id for instance in item_scraper_configs]
  )
