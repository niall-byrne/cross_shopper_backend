"""Test the admin for the Report model."""

from typing import TYPE_CHECKING

from django.contrib import admin
from reports.admin.inlines.report import report_inlines
from reports.admin.list_filters.report import report_list_filter

if TYPE_CHECKING:  # no cover
  from reports.admin.report import ReportAdmin


class TestReportAdmin:

  def test_instantiate__inheritance(
      self,
      report_admin: "ReportAdmin",
  ) -> None:
    assert isinstance(report_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_fieldsets(
      self,
      report_admin: "ReportAdmin",
  ) -> None:
    assert report_admin.fieldsets == (
        (
            "IDENTIFICATION",
            {
                "fields": ("name", "user", "is_testing_only")
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

  def test_instantiate__has_list_filter(
      self,
      report_admin: "ReportAdmin",
  ) -> None:
    assert report_admin.list_filter == report_list_filter

  def test_instantiate__ordering(self, report_admin: "ReportAdmin") -> None:
    assert report_admin.ordering == ("name",)
