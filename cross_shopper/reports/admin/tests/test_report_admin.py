"""Test the admin for the Report model."""

from typing import TYPE_CHECKING

from reports.admin.inlines.report import report_inlines

if TYPE_CHECKING:  # no cover
  from reports.admin.report import ReportAdmin


class TestReportAdmin:

  def test_instantiate__has_correct_fieldsets(
      self,
      report_admin: "ReportAdmin",
  ) -> None:
    assert report_admin.fieldsets == (
        (
            "IDENTIFICATION",
            {
                "fields": ("name", "user")
            },
        ),
        (
            "ITEMS",
            {
                "fields": ("item",)
            },
        ),
    )

  def test_instantiate__has_correct_filter_horizontal(
      self,
      report_admin: "ReportAdmin",
  ) -> None:
    assert report_admin.filter_horizontal == [
        "item",
    ]

  def test_instantiate__has_correct_inlines(
      self,
      report_admin: "ReportAdmin",
  ) -> None:
    assert report_admin.inlines == report_inlines
