"""Tests for the ReportSummarySerializer."""

import pytest
from freezegun import freeze_time
from items.models.factories.item import ItemFactory
from reports.models.serializers.report_summary.report import (
    ReportSummarySerializer,
)


@pytest.mark.django_db
class TestReportSummarySerializer:
  """Tests for the ReportSummarySerializer."""

  @freeze_time("2024-01-01 12:00:00")
  def test_serialize__valid_instance__correct_representation(self, report):
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
    assert int(data['week']) == 1
    assert int(data['year']) == 2024
    assert data['generated_at'] == "Mon, 01 Jan 2024 12:00:00 GMT"
    assert len(data['stores']) == report.store.count()
    assert len(data['items']) == report.item.count()

  def test_serialize__item_ordering__is_correct(self, report):
    # Add items in non-alphabetical order
    item_b = ItemFactory(name="B", brand__name="Brand B")
    item_a = ItemFactory(name="A", brand__name="Brand A")
    report.item.add(item_b, item_a)

    serializer = ReportSummarySerializer(
        report,
        context={
            'week': 1,
            'year': 2024,
        },
    )
    items_data = serializer.data['items']
    assert items_data[0]['name'] == "A"
    assert items_data[1]['name'] == "B"
