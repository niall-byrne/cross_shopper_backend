"""Tests for the ReportSummaryItemSerializer."""

import pytest
from items.models.serializers.packaging import PackagingSerializer
from reports.models.serializers.report_summary.item import (
    ReportSummaryItemSerializer,
)


@pytest.mark.django_db
class TestReportSummaryItemSerializer:
  """Tests for the ReportSummaryItemSerializer."""

  def test_serialize__valid_instance__correct_representation(self, item):
    serializer = ReportSummaryItemSerializer(item)
    assert serializer.data == {
        'id': item.id,
        'name': item.name,
        'brand': item.brand.name,
        'is_bulk': item.is_bulk,
        'is_organic': item.is_organic,
        'is_non_gmo': item.is_non_gmo,
        'packaging': PackagingSerializer(item.packaging).data,
        'price': {
            'last_52_weeks': {
                'average': None,
                'high': None,
                'low': None,
            },
            'selected_week': {
                'average': None,
                'best': None,
                'per_store': {},
            },
        },
    }
