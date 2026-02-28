"""Tests for the ReportSummaryStoreSerializer."""

import pytest
from reports.models.serializers.report_summary.store import (
    ReportSummaryStoreSerializer,
)


@pytest.mark.django_db
class TestReportSummaryStoreSerializer:
  """Tests for the ReportSummaryStoreSerializer."""

  def test_serialize__valid_instance__correct_representation(self, store):
    serializer = ReportSummaryStoreSerializer(store)
    assert serializer.data == {
        'id': store.id,
        'franchise_name': store.franchise.name,
    }
