"""Tests for the ReportSummaryItemPriceSerializer."""

from typing import TYPE_CHECKING
from unittest import mock

import pytest
from reports.models.serializers.report_summary.item_price import (
    ReportSummaryItemPriceSerializer,
)
from reports.models.serializers.report_summary.item_price_current import (
    ReportSummaryCurrentItemPriceSerializer,
)
from reports.models.serializers.report_summary.item_price_historical import (
    ReportSummaryHistoricalItemPriceSerializer,
)

if TYPE_CHECKING:
  from items.models import Item
  from reports.models.report import Report


@pytest.mark.django_db
class TestReportSummaryItemPriceSerializer:
  """Tests for the ReportSummaryItemPriceSerializer."""

  def test_serialization__specified_item__returns_correct_representation(
      self,
      report: "Report",
      report_with_prefetched_item: "Item",
      report_summary_mocked_aggregate_last_52_weeks_manager: mock.Mock,
  ) -> None:
    report_summary_mocked_aggregate_last_52_weeks_manager.average.return_value = 10.50
    report_summary_mocked_aggregate_last_52_weeks_manager.high.return_value = 15.00
    report_summary_mocked_aggregate_last_52_weeks_manager.low.return_value = 5.00
    context = {'report': report}
    serializer = ReportSummaryItemPriceSerializer(
        report_with_prefetched_item,
        context=context,
    )

    data = serializer.data

    assert data == {
        "last_52_weeks": ReportSummaryHistoricalItemPriceSerializer(
            report_with_prefetched_item,
            context=context,
        ).data,
        "selected_week": ReportSummaryCurrentItemPriceSerializer(
            report_with_prefetched_item,
            context=context,
        ).data,
    }
