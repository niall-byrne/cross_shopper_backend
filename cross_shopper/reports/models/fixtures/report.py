"""Fixtures for building Report models."""

from typing import TYPE_CHECKING

import pytest
from items.models.factories.item import ItemFactory, ScraperConfigFactory
from reports.models.factories.report import ReportFactory, ReportStoreFactory
from stores.models.factories.store import StoreFactory

if TYPE_CHECKING:  # no cover
  from reports.models import Report, ReportStore


@pytest.fixture
def report() -> "Report":
  return ReportFactory.create(
      items=[
          ItemFactory.create(scraper_configs=[ScraperConfigFactory.create()]),
          ItemFactory.create(scraper_configs=[ScraperConfigFactory.create()]),
      ],
      stores=[
          StoreFactory.create(),
          StoreFactory.create(),
      ],
  )


@pytest.fixture
def report_store() -> "ReportStore":
  return ReportStoreFactory.create()
