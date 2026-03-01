"""Tests for the ReportSummaryHistoricalItemPriceSerializer."""

import pytest
from items.models import Item
from pricing.models.fixtures.pricing import AliasCreateLast52PriceBatchFromReport
from reports.models import Report
from ..item_price_historical import ReportSummaryHistoricalItemPriceSerializer


@pytest.mark.django_db
class TestReportSummaryHistoricalItemPriceSerializer:
  """Tests for the ReportSummaryHistoricalItemPriceSerializer."""

  def test_serialization(
      self,
      report: Report,
      item: Item,
      create_last_52_price_batch_from_report:
      AliasCreateLast52PriceBatchFromReport,
  ) -> None:
    """Test that the serializer correctly calculates historical price stats."""
    report.item.add(item)
    create_last_52_price_batch_from_report(report)

    context = {'report': report}
    serializer = ReportSummaryHistoricalItemPriceSerializer(
        item,
        context=context,
    )

    data = serializer.data
    assert 'average' in data
    assert 'high' in data
    assert 'low' in data

  def test_serialization__no_report_context(self, item: Item) -> None:
    """Test that the serializer handles missing report context."""
    serializer = ReportSummaryHistoricalItemPriceSerializer(item, context={})
    assert serializer.data == {
        'average': None,
        'high': None,
        'low': None,
    }

  def test_serialization__no_prices(self, report: Report, item: Item) -> None:
    """Test that the serializer handles cases with no historical prices."""
    context = {'report': report}
    serializer = ReportSummaryHistoricalItemPriceSerializer(
        item,
        context=context,
    )

    assert serializer.data == {
        'average': None,
        'high': None,
        'low': None,
    }
