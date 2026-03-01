"""Tests for the ReportSummaryHistoricalItemPriceSerializer."""

import pytest
from items.models import Item
from pricing.models.fixtures.pricing import AliasCreateLast52PriceBatchFromReport
from reports.models import Report
from ..item_price_historical import ReportSummaryHistoricalItemPriceSerializer


@pytest.mark.django_db
class TestReportSummaryHistoricalItemPriceSerializer:
  """Tests for the ReportSummaryHistoricalItemPriceSerializer."""

  def test_serialization__specified_item__correct_representation(
      self,
      report: Report,
      item: Item,
      create_last_52_price_batch_from_report:
      AliasCreateLast52PriceBatchFromReport,
  ) -> None:
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

  def test_serialization__no_report_context__none_values(
      self,
      item: Item,
  ) -> None:
    serializer = ReportSummaryHistoricalItemPriceSerializer(item, context={})

    assert serializer.data == {
        'average': None,
        'high': None,
        'low': None,
    }

  def test_serialization__no_prices__none_values(
      self,
      report: Report,
      item: Item,
  ) -> None:
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
