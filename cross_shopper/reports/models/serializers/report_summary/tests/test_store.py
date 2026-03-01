"""Tests for the ReportSummaryStoreSerializer."""

import pytest
from reports.models.serializers.report_summary.store import (
    ReportSummaryStoreSerializer,
)
from stores.models import Store


@pytest.mark.django_db
class TestReportSummaryStoreSerializer:
  """Tests for the ReportSummaryStoreSerializer."""

  def test_serialization__specified_store__returns_correct_representation(
      self,
      store: "Store",
  ) -> None:
    serializer = ReportSummaryStoreSerializer(store)

    assert serializer.data == {
        "id": store.id,
        "franchise_name": store.franchise.name,
    }
