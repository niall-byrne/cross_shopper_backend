"""Tests for the ReportSummaryItemPriceSerializer."""

from typing import TYPE_CHECKING

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
  from reports.models.report import Report


@pytest.mark.django_db
class TestReportSummaryItemPriceSerializer:

  @pytest.mark.usefixtures(
      "report_summary_mocked_pricing_aggregate_last_52_weeks_manager"
  )
  def test_serialization__specified_item__returns_correct_representation(
      self,
      report_prefetched: "Report",
  ) -> None:
    item = report_prefetched.item.all()[0]
    serializer = ReportSummaryItemPriceSerializer(
        item,
        context={'report': report_prefetched},
    )

    assert serializer.data == {
        "last_52_weeks":
            ReportSummaryHistoricalItemPriceSerializer(
                item,
                context=serializer.context,
            ).data,
        "selected_week":
            ReportSummaryCurrentItemPriceSerializer(
                item,
                context=serializer.context,
            ).data,
    }
