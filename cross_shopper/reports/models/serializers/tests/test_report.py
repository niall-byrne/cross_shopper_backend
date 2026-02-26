"""Test the ReportSerializer class."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from items.models.serializers.item import ItemSerializer
from reports.models.serializers.report import ReportSerializer
from stores.models.serializers.store import StoreSerializer

if TYPE_CHECKING:
  from reports.models import Report
  from .conftest import AliasCreateMockedRequest


@pytest.mark.django_db
class TestReportSerializer:

  def test_serialization__correct_representation(
      self,
      report: Report,
      create_mocked_request: AliasCreateMockedRequest,
  ) -> None:
    serialized = ReportSerializer(
        report, context={"request": create_mocked_request({})}
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
        "is_testing_only": report.is_testing_only,
    }
