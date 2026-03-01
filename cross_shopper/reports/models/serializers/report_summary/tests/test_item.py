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

  def test_serialization__specified_item__correct_representation(
      self,
      report: Report,
      item: Item,
      mocked_aggregate_last_52_weeks_manager: mock.Mock,
  ) -> None:
    mocked_aggregate_last_52_weeks_manager.average.return_value = 10.50
    mocked_aggregate_last_52_weeks_manager.high.return_value = 15.00
    mocked_aggregate_last_52_weeks_manager.low.return_value = 5.00
    serializer = ReportSummaryItemSerializer(item, context={'report': report})

    data = serializer.data

    assert data == {
        "id": item.id,
        "name": item.name,
        "brand": item.brand.name,
        "is_bulk": item.is_bulk,
        "is_organic": item.is_organic,
        "is_non_gmo": item.is_non_gmo,
        "packaging": PackagingSerializer(item.packaging).data,
        "price": {
            "last_52_weeks": {
                "average": "10.5",
                "high": "15.0",
                "low": "5.0",
            },
            "selected_week": {
                "average": None,
                "best": None,
                "per_store": {},
            },
        },
    }
