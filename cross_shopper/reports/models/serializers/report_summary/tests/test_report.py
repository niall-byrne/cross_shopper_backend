"""Tests for the ReportSummarySerializer."""

from datetime import datetime
from typing import Any
from unittest import mock

import pytest
from django.db.models import Prefetch
from freezegun import freeze_time
from items.models import Item
from items.models.factories.item import ItemFactory
from reports.models import Report
from reports.models.serializers.report_summary.report import (
  ReportSummarySerializer,
)


@pytest.mark.django_db
class TestReportSummarySerializer:
  """Tests for the ReportSummarySerializer."""

  @freeze_time("2024-01-01 12:00:00")
  def test_serialization__specified_report__returns_correct_representation(
      self,
      report_prefetched: Report,
  ) -> None:
    from reports.models.serializers.report_summary.item import (
        ReportSummaryItemSerializer,
    )
    from reports.models.serializers.report_summary.store import (
        ReportSummaryStoreSerializer,
    )
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
      report: Report,
  ) -> None:
    from api.views.report_summary.qs import qs_item
    report.item.clear()
    item1 = ItemFactory(name='B item')
    item2 = ItemFactory(name='A item')
    report.item.add(item1, item2)  # type: ignore[arg-type]
    qs = Report.objects.filter(id=report.id).prefetch_related(
        Prefetch(
            'item',
            queryset=qs_item(),
        )
    )
    report_prefetched = qs.get()
    serializer = ReportSummarySerializer(report_prefetched)

    item_data = serializer.get_item(report_prefetched)
    item_names = [i['name'] for i in item_data]

    assert item_names == ['A item', 'B item']
