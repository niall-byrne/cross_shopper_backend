"""Tests for the ReportSummaryStoreSerializer."""

import pytest
from stores.models import Store
from ..store import ReportSummaryStoreSerializer


@pytest.mark.django_db
class TestReportSummaryStoreSerializer:
  """Tests for the ReportSummaryStoreSerializer."""

  def test_serialization__specified_store__correct_representation(
      self,
      store: Store,
  ) -> None:
    serializer = ReportSummaryStoreSerializer(store)

    assert serializer.data == {
        "id": store.id,
        "franchise_name": store.franchise.name,
    }
