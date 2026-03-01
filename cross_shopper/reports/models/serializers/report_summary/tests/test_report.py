"""Tests for the ReportSummarySerializer."""

from datetime import datetime
from typing import Any
from unittest.mock import patch

import pytest
from reports.models import Report
from ..report import ReportSummarySerializer


@pytest.mark.django_db
class TestReportSummarySerializer:
  """Tests for the ReportSummarySerializer."""

  @patch("django.utils.timezone.now")
  def test_serialization(self, mock_now, report: Report) -> None:
    """Test that the serializer correctly represents a report summary."""
    mock_now.return_value = datetime(2024, 1, 1, 12, 0, 0)
    serializer = ReportSummarySerializer(
        report,
        context={
            'week': 1,
            'year': 2024,
        },
    )

    data = serializer.data
    assert data['id'] == report.id
    assert data['name'] == report.name
    assert data['week'] == 1
    assert data['year'] == 2024
    assert data['generated_at'] == "Mon, 01 Jan 2024 12:00:00 GMT"
    assert 'store' in data
    assert 'item' in data
    assert len(data['store']) == report.store.count()
    assert len(data['item']) == report.item.count()

  def test_get_item_ordering(self, report: Report) -> None:
    """Test that items are correctly ordered in the serialized representation."""
    # Clearing items to have a controlled test
    report.item.clear()

    # Adding more items to test ordering
    from items.models.factories.item import ItemFactory
    item1 = ItemFactory(name='B item')
    item2 = ItemFactory(name='A item')
    report.item.add(item1, item2)

    # We need to use the viewset's logic or manually order for this test
    # since the serializer just calls instance.item.all()
    # and expects it to be ordered by the prefetch.
    from django.db.models import Prefetch
    from items.models import Item
    qs = Report.objects.filter(id=report.id).prefetch_related(
        Prefetch(
            'item',
            queryset=Item.objects.all().order_by(
                *ReportSummarySerializer.ITEM_FIELD_ORDERING
            ),
        )
    )
    report_with_prefetch = qs.get()

    serializer = ReportSummarySerializer(report_with_prefetch)
    item_data = serializer.get_item(report_with_prefetch)
    item_names = [i['name'] for i in item_data]

    # Verify order is based on name
    assert item_names == ['A item', 'B item']
