"""Tests for the ReportSummarySerializer."""

from datetime import datetime
from typing import Any
from unittest import mock
from unittest.mock import patch

import pytest
from django.db.models import Prefetch
from items.models import Item
from items.models.factories.item import ItemFactory
from reports.models import Report
from ..report import ReportSummarySerializer


@pytest.mark.django_db
class TestReportSummarySerializer:
  """Tests for the ReportSummarySerializer."""

  @patch("django.utils.timezone.now")
  def test_serialization__specified_report__correct_representation(
      self,
      mock_now: mock.Mock,
      report: Report,
  ) -> None:
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

  def test_get_item__multiple_items__correct_ordering(
      self,
      report: Report,
  ) -> None:
    from api.views.report_summary.qs import qs_item
    report.item.clear()
    item1 = ItemFactory(name='B item')
    item2 = ItemFactory(name='A item')
    report.item.add(item1, item2)
    qs = Report.objects.filter(id=report.id).prefetch_related(
        Prefetch(
            'item',
            queryset=qs_item(),
        )
    )
    report_with_prefetch = qs.get()
    serializer = ReportSummarySerializer(report_with_prefetch)
    item_data = serializer.get_item(report_with_prefetch)
    item_names = [i['name'] for i in item_data]

    assert item_names == ['A item', 'B item']
