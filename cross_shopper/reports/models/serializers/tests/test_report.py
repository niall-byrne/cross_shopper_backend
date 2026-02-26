"""Test the ReportSerializer class."""

import pytest
from items.models.serializers.item import ItemSerializer
from reports.models import Report
from reports.models.serializers.report import ReportSerializer
from stores.models.serializers.store import StoreSerializer
from .conftest import AliasCreateMockedRequest


@pytest.mark.django_db
class TestReportSerializer:

  def test_serialization__correct_representation(
      self,
      report: Report,
      create_mocked_request: AliasCreateMockedRequest,
  ) -> None:
    serialized = ReportSerializer(
        report, context={'request': create_mocked_request({})}
    )

    assert serialized.data == {
        "id": report.pk,
        "name": report.name,
        "item": ItemSerializer(
            report.item.all(),
            many=True,
        ).data,
        "store": StoreSerializer(
            report.store,
            many=True,
        ).data,
        "is_testing": report.is_testing,
    }
