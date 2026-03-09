"""Test the TestReportSerializerRO class."""

import pytest
from reports.models import Report
from reports.models.serializers.read_only.report_target import (
    ReportTargetSerializerRO,
)


@pytest.mark.django_db
class TestReportTargetSerializerRO:

  def test_serialization__correct_representation(
      self,
      report: Report,
  ) -> None:
    serialized = ReportTargetSerializerRO(report)

    assert serialized.data == {
        "id": report.pk,
        "name": report.name,
    }
