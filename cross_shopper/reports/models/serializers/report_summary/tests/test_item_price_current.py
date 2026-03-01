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

  price1 = PriceFactory(
      item=item,
      store=stores[0],
      amount=decimal.Decimal('10.00'),
      year=2024,
      week=1,
  )
  price2 = PriceFactory(
      item=item,
      store=stores[1],
      amount=decimal.Decimal('20.00'),
      year=2024,
      week=1,
  )
  return {
      str(stores[0].id): price1,
      str(stores[1].id): price2,
  }


@pytest.mark.django_db
class TestReportSummaryCurrentItemPriceSerializer:
  """Tests for the ReportSummaryCurrentItemPriceSerializer."""

  def test_serialization(
      self, report: Report, item: Item, current_prices: Dict[str, Price]
  ) -> None:
    """Test that the serializer correctly calculates current price stats."""
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
        store_id: str(price.amount)
        for store_id, price in current_prices.items()
    }

    assert serializer.data == {
        'average': '15.00',
        'best': '10.00',
        'per_store': expected_per_store,
    }

  def test_serialization__no_prices(self, report: Report, item: Item) -> None:
    """Test that the serializer handles cases with no prices."""
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
