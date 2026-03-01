"""Test fixtures for the ReportSummaryCurrentItemPriceSerializer."""

import decimal
from typing import Dict
from unittest import mock

import pytest
from items.models import Item
from pricing.models import Price
from pricing.models.factories.pricing import PriceFactory
from reports.models import Report


@pytest.fixture
def mocked_aggregate_last_52_weeks_manager(
    monkeypatch: pytest.MonkeyPatch
) -> mock.Mock:
  manager_mock = mock.Mock()
  monkeypatch.setattr(Price, "aggregate_last_52_weeks", manager_mock)

  return manager_mock


@pytest.fixture
def current_prices(report: Report, item: Item) -> Dict[str, Price]:
  report.item.add(item)
  stores = list(report.store.all())
  num_stores = len(stores)

  results: Dict[str, Price] = {}
  for i in range(min(num_stores, 2)):
    price = PriceFactory(
        item=item,
        store=stores[i],
        amount=decimal.Decimal(f'{(i + 1) * 10}.00'),
        year=2024,
        week=1,
    )
    results[str(stores[i].id)] = price  # type: ignore[assignment]

  return results


@pytest.fixture
def report_prefetched(report: Report) -> Report:
  from api.views.report_summary.qs import qs_item
  from django.db.models import Prefetch

  qs = Report.objects.filter(id=report.id).prefetch_related(
      'store',
      Prefetch('item', queryset=qs_item()),
  )
  return qs.get()
