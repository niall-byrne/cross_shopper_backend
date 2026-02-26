"""Fixtures for building Report models."""

from typing import TYPE_CHECKING, Callable, Tuple

import pytest
from items.models.factories.item import ItemFactory
from pricing.models.factories.pricing import TodayPriceFactory
from reports.models.factories.report import ReportFactory, ReportStoreFactory
from scrapers.models.factories.scraper_config import ScraperConfigFactory
from stores.models.factories.store import StoreFactory

if TYPE_CHECKING:  # no cover
  from django.contrib.auth.base_user import AbstractBaseUser
  from items.models import Item
  from reports.models import Report, ReportStore
  from stores.models import Store

AliasGetReportStores = Callable[["Report"], Tuple["Store", "Store"]]
AliasGetReportItem = Callable[["Report"], "Item"]


def create_report(
    user: "AbstractBaseUser", testing_only: bool = False
) -> "Report":
  return ReportFactory.create(
      items=[
          ItemFactory.create(scraper_configs=[ScraperConfigFactory.create()]),
          ItemFactory.create(scraper_configs=[ScraperConfigFactory.create()]),
      ],
      stores=[
          StoreFactory.create(),
          StoreFactory.create(),
      ],
      user=user,
      is_testing_only=testing_only,
  )


@pytest.fixture
def report(user: "AbstractBaseUser") -> "Report":
  return create_report(user)


@pytest.fixture
def report_alternate(user: "AbstractBaseUser") -> "Report":
  return create_report(user)


@pytest.fixture
def report_testing(user: "AbstractBaseUser") -> "Report":
  return create_report(user, testing_only=True)


@pytest.fixture
def report_store() -> "ReportStore":
  return ReportStoreFactory.create()


@pytest.fixture
def report_with_pricing() -> "Report":
  items_and_stores: Tuple[Tuple[Item, ...], Tuple[Store, ...]] = (
      tuple(
          ItemFactory.create(scraper_configs=[ScraperConfigFactory.create()])
          for _ in range(0, 10)
      ),
      tuple(StoreFactory.create() for _ in range(0, 10)),
  )

  for item, store in zip(*items_and_stores):
    TodayPriceFactory.create(item=item, store=store)

  report = ReportFactory.create(
      items=items_and_stores[0],
      stores=items_and_stores[1],
  )

  return report
