"""Tests for the ReportSummaryItemPriceSerializer."""

import pytest
from reports.models.serializers.report_summary.item_price import (
    ReportSummaryItemPriceSerializer,
)


@pytest.mark.django_db
class TestReportSummaryItemPriceSerializer:
  """Tests for the ReportSummaryItemPriceSerializer."""

  def test_serialize__valid_instance__correct_representation(self, item):
    serializer = ReportSummaryItemPriceSerializer(item)
    assert serializer.data == {
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
    }
