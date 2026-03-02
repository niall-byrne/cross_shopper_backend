"""Tests for the ReportSummaryStoreSerializerRO."""

import pytest
from reports.models.serializers.read_only.report_summary.store import (
    ReportSummaryStoreSerializerRO,
)
from stores.models import Store


@pytest.mark.django_db
class TestReportSummaryStoreSerializerRO:
  """Tests for the ReportSummaryStoreSerializerRO."""

  def test_serialization__specified_store__returns_correct_representation(
      self,
      store: "Store",
  ) -> None:
    serializer = ReportSummaryStoreSerializerRO(store)

    assert serializer.data == {
        "id": store.pk,
        "franchise_name": store.franchise.name,
        "postal_code": store.address.locality.postal_code,
    }
