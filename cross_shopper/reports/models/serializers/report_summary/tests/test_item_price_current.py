"""Tests for the ReportSummaryCurrentItemPriceSerializer."""

from typing import Dict, Optional

import pytest
from items.models import Item
from pricing.models import Price
from reports.models.report import Report
from reports.models.serializers.report_summary.item_price_current import (
    ReportSummaryCurrentItemPriceSerializer,
)


@pytest.mark.django_db
class TestReportSummaryCurrentItemPriceSerializer:
  """Tests for the ReportSummaryCurrentItemPriceSerializer."""

  def test_serialization__specified_item__returns_correct_representation(
      self,
      report: "Report",
      item: "Item",
      report_summary_current_prices: Dict[str, Price],
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
    expected_per_store: Dict[str, Optional[str]] = {
        str(store.id): None for store in report.store.all()
    }
    for store_id, price in report_summary_current_prices.items():
      expected_per_store[store_id] = str(price.amount)

    data = serializer.data

    assert data['per_store'] == expected_per_store
    if len(report_summary_current_prices) >= 2:
      assert data['average'] == '15.00'
      assert data['best'] == '10.00'

  def test_serialization__no_prices__returns_none(
      self,
      report: "Report",
      item: "Item",
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
