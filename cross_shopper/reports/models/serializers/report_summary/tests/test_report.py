"""Tests for the ReportSummarySerializer."""

from typing import TYPE_CHECKING

import pytest
from freezegun import freeze_time
from items.models.factories.item import ItemFactory
from reports.models.report import Report
from reports.models.serializers.report_summary.item import (
    ReportSummaryItemSerializer,
)
from reports.models.serializers.report_summary.report import (
    ReportSummarySerializer,
)
from reports.models.serializers.report_summary.store import (
    ReportSummaryStoreSerializer,
)

if TYPE_CHECKING:
  from items.models import Item


@pytest.mark.django_db
class TestReportSummarySerializer:
  """Tests for the ReportSummarySerializer."""

  @freeze_time("2024-01-01 12:00:00")
  def test_serialization__specified_report__returns_correct_representation(
      self,
      report_prefetched: "Report",
  ) -> None:
    context = {
        'week': 1,
        'year': 2024,
    }
    serializer = ReportSummarySerializer(
        report_prefetched,
        context=context,
    )

    data = serializer.data

    assert data['id'] == report_prefetched.id
    assert data['name'] == report_prefetched.name
    assert data['week'] == 1
    assert data['year'] == 2024
    assert data['generated_at'] == "Mon, 01 Jan 2024 12:00:00 GMT"
    assert data['store'] == ReportSummaryStoreSerializer(
        report_prefetched.store.all(),
        many=True,
    ).data
    assert data['item'] == ReportSummaryItemSerializer(
        report_prefetched.item.all(),
        many=True,
        context={
            **context,
            'report': report_prefetched,
        },
    ).data

  def test_get_item__multiple_items__returns_items_in_name_order(
      self,
      report_with_multiple_items_prefetched: "Report",
  ) -> None:
    serializer = ReportSummarySerializer(report_with_multiple_items_prefetched)

    item_data = serializer.get_item(report_with_multiple_items_prefetched)

    item_names = [i['name'] for i in item_data]
    assert item_names == ['A item', 'B item']
