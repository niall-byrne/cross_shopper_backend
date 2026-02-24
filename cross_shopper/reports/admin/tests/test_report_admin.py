"""Test the admin for the Report model."""

from django.contrib import admin
from reports.admin import filters
from reports.admin.report import ReportAdmin, ReportStoreInline


class TestReportAdmin:
  """Test the ReportAdmin class."""

  def test_instantiate__inheritance(
      self,
      report_admin: ReportAdmin,
  ) -> None:
    assert isinstance(report_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_fieldsets(
      self,
      report_admin: ReportAdmin,
  ) -> None:
    assert report_admin.fieldsets == (
        (
            "IDENTIFICATION",
            {
                "fields": ('name', 'user', 'is_testing_only')
            },
        ),
        (
            "ITEMS",
            {
                "fields": ('item',)
            },
        ),
    )

  def test_instantiate__has_correct_filter_horizontal(
      self,
      report_admin: ReportAdmin,
  ) -> None:
    assert report_admin.filter_horizontal == [
        "item",
    ]

  def test_instantiate__has_correct_inlines(
      self,
      report_admin: ReportAdmin,
  ) -> None:
    assert report_admin.inlines == [ReportStoreInline]

  def test_instantiate__has_correct_list_filter(
      self,
      report_admin: ReportAdmin,
  ) -> None:
    assert report_admin.list_filter == filters.report_filter

  def test_instantiate__ordering(self, report_admin: ReportAdmin) -> None:
    assert report_admin.ordering == ('name',)
