"""Test fixtures for the ReportSummaryCurrentItemPriceSerializer."""

import decimal
from typing import Dict

import pytest
from items.models import Item
from pricing.models import Price
from pricing.models.factories.pricing import PriceFactory
from reports.models import Report


@pytest.fixture
def current_prices(report: Report, item: Item) -> Dict[str, Price]:
  """Fixture to create current prices for a report and item."""
  report.item.add(item)
  stores = list(report.store.all())
  num_stores = len(stores)

  results = {}
  for i in range(min(num_stores, 2)):
    price = PriceFactory(
        item=item,
        store=stores[i],
        amount=decimal.Decimal(f'{(i + 1) * 10}.00'),
        year=2024,
        week=1,
    )
    results[str(stores[i].id)] = price

  return results
