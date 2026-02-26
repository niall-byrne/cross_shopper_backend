"""Test the ReportSerializer class."""

from typing import TYPE_CHECKING

import pytest
from items.models.serializers.item import ItemSerializer
from reports.models.serializers.report import ReportSerializer
from stores.models.serializers.store import StoreSerializer

if TYPE_CHECKING:  # no cover
  from reports.models import Report


@pytest.mark.django_db
class TestReportSerializer:

  def test_serialization__correct_representation(
      self,
      report: "Report",
  ) -> None:
    serialized = ReportSerializer(report, context={})

    assert serialized.data == {
        "id":
            report.pk,
        "name":
            report.name,
        "item":
            ItemSerializer(
                report.item.all().order_by(
                    *ReportSerializer.ITEM_FIELD_ORDERING
                ),
                many=True,
            ).data,
        "store":
            StoreSerializer(
                report.store,
                many=True,
            ).data,
        "is_testing_only":
            report.is_testing_only,
    }
