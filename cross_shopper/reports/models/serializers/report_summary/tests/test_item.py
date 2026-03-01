"""Tests for the ReportSummaryItemSerializer."""

from unittest import mock

import pytest
from items.models import Item
from items.models.serializers.packaging import PackagingSerializer
from pricing.models import Price
from reports.models import Report
from reports.models.serializers.report_summary.item import (
  ReportSummaryItemSerializer,
)


@pytest.mark.django_db
class TestReportSummaryItemSerializer:
  """Tests for the ReportSummaryItemSerializer."""

  def test_serialization__specified_item__returns_correct_representation(
      self,
      report: Report,
      item_prefetched: Item,
      mocked_aggregate_last_52_weeks_manager: mock.Mock,
  ) -> None:
    from reports.models.serializers.report_summary.item_price import (
        ReportSummaryItemPriceSerializer,
    )
    mocked_aggregate_last_52_weeks_manager.average.return_value = 10.50
    mocked_aggregate_last_52_weeks_manager.high.return_value = 15.00
    mocked_aggregate_last_52_weeks_manager.low.return_value = 5.00
    context = {'report': report}
    serializer = ReportSummaryItemSerializer(
        item_prefetched,
        context=context,
    )

    data = serializer.data

    assert data == {
        "id": item_prefetched.id,
        "name": item_prefetched.name,
        "brand": item_prefetched.brand.name,
        "is_bulk": item_prefetched.is_bulk,
        "is_organic": item_prefetched.is_organic,
        "is_non_gmo": item_prefetched.is_non_gmo,
        "packaging": PackagingSerializer(item_prefetched.packaging).data,
        "price": ReportSummaryItemPriceSerializer(
            item_prefetched,
            context=context,
        ).data,
    }
