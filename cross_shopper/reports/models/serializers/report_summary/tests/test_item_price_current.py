"""Tests for the ReportSummaryCurrentItemPriceSerializer."""

import decimal
from typing import Dict

import pytest
from items.models import Item
from pricing.models import Price
from pricing.models.factories.pricing import PriceFactory
from reports.models import Report
from ..item_price_current import ReportSummaryCurrentItemPriceSerializer


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


@pytest.mark.django_db
class TestReportSummaryCurrentItemPriceSerializer:
  """Tests for the ReportSummaryCurrentItemPriceSerializer."""

  def test_serialization__specified_item__correct_representation(
      self,
      report: Report,
      item: Item,
      current_prices: Dict[str, Price],
  ) -> None:
    context = {
        'report': report,
        'year': 2024,
        'week': 1,
    }
    serializer = ReportSummaryCurrentItemPriceSerializer(
        item,
        context=context,
    )
    expected_per_store = {
        str(store.id): None for store in report.store.all()
    }
    for store_id, price in current_prices.items():
      expected_per_store[store_id] = str(price.amount)

    data = serializer.data

    assert data['per_store'] == expected_per_store
    if len(current_prices) >= 2:
      assert data['average'] == '15.00'
      assert data['best'] == '10.00'

  def test_serialization__no_prices__none_values(
      self,
      report: Report,
      item: Item,
  ) -> None:
    report.item.add(item)
    stores = report.store.all()
    context = {
        'report': report,
        'year': 2024,
        'week': 1,
    }
    serializer = ReportSummaryCurrentItemPriceSerializer(
        item,
        context=context,
    )

    assert serializer.data == {
        'average': None,
        'best': None,
        'per_store': {str(store.id): None for store in stores},
    }
