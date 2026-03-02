"""Tests for the ReportSummaryItemPriceSerializerRO."""

from typing import TYPE_CHECKING

import pytest
from reports.models.serializers.read_only.report_summary.\
  item_price_current import (
    ReportSummaryCurrentItemPriceSerializerRO,
)
from reports.models.serializers.read_only.report_summary.\
  item_price_historical import (
    ReportSummaryHistoricalItemPriceSerializerRO,
)
from reports.models.serializers.read_only.report_summary.item_price import (
    ReportSummaryItemPriceSerializerRO,
)

if TYPE_CHECKING:
  from reports.models.report import Report


@pytest.mark.django_db
class TestReportSummaryItemPriceSerializerRO:

  @pytest.mark.usefixtures(
      "report_summary_mocked_pricing_aggregate_last_52_weeks_manager"
  )
  def test_serialization__specified_item__returns_correct_representation(
      self,
      report_prefetched: "Report",
  ) -> None:
    item = report_prefetched.item.all()[0]
    serializer = ReportSummaryItemPriceSerializerRO(
        item,
        context={'report': report_prefetched},
    )

    assert serializer.data == {
        "last_52_weeks":
            ReportSummaryHistoricalItemPriceSerializerRO(
                item,
                context=serializer.context,
            ).data,
        "selected_week":
            ReportSummaryCurrentItemPriceSerializerRO(
                item,
                context=serializer.context,
            ).data,
    }
