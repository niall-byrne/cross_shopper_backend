"""Fixtures for building Report models."""

import decimal
from typing import TYPE_CHECKING, Callable, Tuple

import pytest
from django.contrib.auth.base_user import AbstractBaseUser
from items.models.factories.item import ItemFactory, ScraperConfigFactory
from pricing.models.factories.pricing import TodayPriceFactory
from reports.models.factories.report import ReportFactory, ReportStoreFactory
from stores.models.factories.store import StoreFactory

if TYPE_CHECKING:  # no cover
  from items.models import Item
  from pricing.models import Price
  from reports.models import Report, ReportStore
  from stores.models import Store

AliasGetReportStores = Callable[["Report"], Tuple["Store", "Store"]]
AliasGetReportItem = Callable[["Report"], "Item"]


def create_report(
    user: AbstractBaseUser, testing_only: bool = False
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
      is_testing=testing_only,
  )


@pytest.fixture
def report(user: AbstractBaseUser) -> "Report":
  return create_report(user)


@pytest.fixture
def report_alternate(user: AbstractBaseUser) -> "Report":
  return create_report(user)


@pytest.fixture
def report_prefetched(report: "Report") -> "Report":
  from django.db.models import Prefetch
  from api.views.report_summary.qs import qs_item

  qs = report.__class__.objects.filter(id=report.id).prefetch_related(
      'store',
      Prefetch('item', queryset=qs_item()),
  )
  return qs.get()


@pytest.fixture
def report_price(item: "Item", report: "Report") -> "Price":
  from pricing.models import Price
  store = list(report.store.all())[0]
  return Price.objects.create(
      item=item,
      store=store,
      amount=decimal.Decimal('99.99'),
      year=2025,
      week=10,
  )


@pytest.fixture
def report_store() -> "ReportStore":
  return ReportStoreFactory.create()


@pytest.fixture
def report_testing(user: AbstractBaseUser) -> "Report":
  return create_report(user, testing_only=True)


@pytest.fixture
def report_with_item(report: "Report", item: "Item") -> "Report":
  report.item.add(item)
  return report


@pytest.fixture
def report_with_multiple_items_prefetched(report: "Report") -> "Report":
  from django.db.models import Prefetch
  from api.views.report_summary.qs import qs_item

  report.item.clear()
  item1 = ItemFactory(name='B item')
  item2 = ItemFactory(name='A item')
  report.item.add(item1, item2)  # type: ignore[arg-type]

  qs = report.__class__.objects.filter(id=report.id).prefetch_related(
      'store',
      Prefetch('item', queryset=qs_item()),
  )
  return qs.get()


@pytest.fixture
def report_with_prefetched_item(
    report_with_item: "Report", item: "Item"
) -> "Item":
  from django.db.models import Prefetch
  from api.views.report_summary.qs import qs_item

  qs = report_with_item.__class__.objects.filter(
      id=report_with_item.id
  ).prefetch_related(
      'store',
      Prefetch('item', queryset=qs_item()),
  )
  report_prefetched = qs.get()
  return report_prefetched.item.get(id=item.id)


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
