"""Tests for the ReportSummaryHistoricalItemPriceSerializer."""

from unittest import mock

import pytest
from items.models import Item
from reports.models import Report
from reports.models.serializers.report_summary.item_price_historical import (
    ReportSummaryHistoricalItemPriceSerializer,
)


@pytest.mark.django_db
class TestReportSummaryHistoricalItemPriceSerializer:
  """Tests for the ReportSummaryHistoricalItemPriceSerializer."""

  def test_serialization__specified_item__returns_correct_representation(
      self,
      report_with_item: "Report",
      item: "Item",
      report_summary_mocked_aggregate_last_52_weeks_manager: mock.Mock,
  ) -> None:
    report_summary_mocked_aggregate_last_52_weeks_manager.average.return_value = 10.50
    report_summary_mocked_aggregate_last_52_weeks_manager.high.return_value = 15.00
    report_summary_mocked_aggregate_last_52_weeks_manager.low.return_value = 5.00
    context = {'report': report_with_item}

    serializer = ReportSummaryHistoricalItemPriceSerializer(
        item,
        context=context,
    )
    data = serializer.data

    assert data == {
        'average': '10.5',
        'high': '15.0',
        'low': '5.0',
    }

  def test_serialization__no_report_context__returns_none(
      self,
      item: Item,
  ) -> None:
    serializer = ReportSummaryHistoricalItemPriceSerializer(item, context={})

    assert serializer.data == {
        'average': None,
        'high': None,
        'low': None,
    }

  def test_serialization__no_prices__returns_none(
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
