"""Test the Report model."""

import pytest
from django.core.exceptions import ValidationError
from reports.models.report import CONSTRAINT_NAMES, Report


@pytest.mark.django_db
class TestReport:

  def test_name__is_unique(
      self,
      report: Report,
  ) -> None:
    report_data = {"name": report.name, "user": report.user}
    with pytest.raises(ValidationError) as exc:
      report2 = Report(**report_data)
      report2.save()

    assert str(exc.value) == str(
        {
            "__all__":
                [
                    'Constraint '
                    f'“{CONSTRAINT_NAMES["name"]}” '
                    'is violated.',
                ]
        }
    )

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
