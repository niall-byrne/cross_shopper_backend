"""Test the TestReportSerializerRO class."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from reports.models.serializers.read_only.report_target import (
    ReportTargetSerializerRO,
)

if TYPE_CHECKING:
  from reports.models import Report


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
