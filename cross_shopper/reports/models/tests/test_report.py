"""Test the Report model."""

import pytest
from reports.models import Report


@pytest.mark.django_db
class TestReport:

  def test_initialize__defaults__attributes(
      self,
      report: Report,
  ) -> None:
    assert report.is_testing is False

  def test_initialize__testing_only__attributes(
      self,
      report_testing: Report,
  ) -> None:
    assert report_testing.is_testing is True

  def test_str__returns_report_name(
      self,
      report: Report,
  ) -> None:
    assert str(report) == report.name
