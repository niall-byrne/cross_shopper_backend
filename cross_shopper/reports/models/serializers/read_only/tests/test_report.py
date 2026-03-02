"""Test the TestReportSerializerRO class."""

import pytest
from items.models.serializers.item import ItemSerializer
from reports.models import Report
from reports.models.serializers.read_only.report import ReportSerializerRO
from stores.models.serializers.read_only.store import StoreSerializerRO
from .conftest import AliasCreateMockedRequest


@pytest.mark.django_db
class TestReportSerializerRO:

  def test_serialization__correct_representation(
      self,
      report: Report,
      create_mocked_request: AliasCreateMockedRequest,
  ) -> None:
    serialized = ReportSerializerRO(
        report, context={"request": create_mocked_request({})}
    )

    assert serialized.data == {
        "id": report.pk,
        "name": report.name,
        "item": ItemSerializer(
            report.item.all(),
            many=True,
        ).data,
        "store": StoreSerializerRO(
            report.store,
            many=True,
        ).data,
        "is_testing": report.is_testing,
    }
