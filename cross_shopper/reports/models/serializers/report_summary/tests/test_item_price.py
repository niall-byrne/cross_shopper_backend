"""Tests for the ReportSummaryItemPriceSerializer."""

from unittest import mock

import pytest
from items.models import Item
from reports.models import Report
from reports.models.serializers.report_summary.item_price import (
    ReportSummaryItemPriceSerializer,
)


@pytest.mark.django_db
class TestReportSummaryItemPriceSerializer:
  """Tests for the ReportSummaryItemPriceSerializer."""

  def test_serialization__specified_item__returns_correct_representation(
      self,
      report: Report,
      item_prefetched: Item,
      mocked_aggregate_last_52_weeks_manager: mock.Mock,
  ) -> None:
    from reports.models.serializers.report_summary.item_price_current import (
        ReportSummaryCurrentItemPriceSerializer,
    )
    from reports.models.serializers.report_summary.item_price_historical import (
        ReportSummaryHistoricalItemPriceSerializer,
    )
    mocked_aggregate_last_52_weeks_manager.average.return_value = 10.50
    mocked_aggregate_last_52_weeks_manager.high.return_value = 15.00
    mocked_aggregate_last_52_weeks_manager.low.return_value = 5.00
    context = {'report': report}
    serializer = ReportSummaryItemPriceSerializer(
        item_prefetched,
        context=context,
    )

    data = serializer.data

    assert data == {
        "last_52_weeks": ReportSummaryHistoricalItemPriceSerializer(
            item_prefetched,
            context=context,
        ).data,
        "selected_week": ReportSummaryCurrentItemPriceSerializer(
            item_prefetched,
            context=context,
        ).data,
    }
