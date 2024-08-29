"""Test the Report model."""

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:  # no cover
  from reports.models import Report


@pytest.mark.django_db
class TestReport:

  def test_str__returns_report_name(
      self,
      report: "Report",
  ) -> None:
    assert str(report) == report.name
