"""Tests for the ReportSummaryItemSerializer."""

from typing import TYPE_CHECKING
from unittest import mock

import pytest
from items.models.serializers.packaging import PackagingSerializer
from reports.models.serializers.report_summary.item import (
    ReportSummaryItemSerializer,
)
from reports.models.serializers.report_summary.item_price import (
    ReportSummaryItemPriceSerializer,
)

if TYPE_CHECKING:
  from items.models import Item
  from reports.models.report import Report


@pytest.mark.django_db
class TestReportSummaryItemSerializer:
  """Tests for the ReportSummaryItemSerializer."""

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
    serializer = ReportSummaryItemSerializer(
        report_with_prefetched_item,
        context=context,
    )

    data = serializer.data

    assert data == {
        "id": report_with_prefetched_item.id,
        "name": report_with_prefetched_item.name,
        "brand": report_with_prefetched_item.brand.name,
        "is_bulk": report_with_prefetched_item.is_bulk,
        "is_organic": report_with_prefetched_item.is_organic,
        "is_non_gmo": report_with_prefetched_item.is_non_gmo,
        "packaging": PackagingSerializer(report_with_prefetched_item.packaging).data,
        "price": ReportSummaryItemPriceSerializer(
            report_with_prefetched_item,
            context=context,
        ).data,
    }
