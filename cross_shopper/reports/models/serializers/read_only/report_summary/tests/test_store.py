"""Tests for the ReportSummaryStoreSerializerRO."""

from typing import TYPE_CHECKING

import pytest
from reports.models.serializers.read_only.report_summary.store import (
    ReportSummaryStoreSerializerRO,
)

if TYPE_CHECKING:  # no cover
  from stores.models import Store


@pytest.mark.django_db
class TestReportSummaryStoreSerializerRO:

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
