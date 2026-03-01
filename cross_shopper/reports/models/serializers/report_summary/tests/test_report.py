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

  def test_get_item_ordering(self, report: Report, item: Any) -> None:
    """Test that items are correctly ordered in the serialized representation."""
    report.item.add(item)
    serializer = ReportSummarySerializer(report)

    # Adding more items to test ordering
    from items.models.factories.item import ItemFactory
    item1 = ItemFactory(name='B item')
    item2 = ItemFactory(name='A item')
    report.item.add(item1, item2)

    item_data = serializer.get_item(report)
    item_names = [i['name'] for i in item_data]

    # Verify order is based on name
    assert 'A item' in item_names
    assert 'B item' in item_names
    assert item_names.index('A item') < item_names.index('B item')
