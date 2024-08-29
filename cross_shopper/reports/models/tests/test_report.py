"""Test the Report model."""

import pytest
from reports.models import Report


@pytest.mark.django_db
class TestReport:

  def test_str__returns_report_name(
      self,
      report: Report,
  ) -> None:
    assert str(report) == report.name
