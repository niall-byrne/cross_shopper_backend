"""Test the admin for the ReportStore model."""

from django.contrib import admin
from reports.admin.list_filter.report_store import report_store_list_filter
from reports.admin.report_store import ReportStoreAdmin


class TestReportStoreAdmin:
  """Test the ReportStoreAdmin class."""

  def test_instantiate__inheritance(
      self,
      report_store_admin: ReportStoreAdmin,
  ) -> None:
    assert isinstance(report_store_admin, admin.ModelAdmin)

  def test_instantiate__has_list_filter(
      self,
      report_store_admin: ReportStoreAdmin,
  ) -> None:
    assert report_store_admin.list_filter == report_store_list_filter

  def test_instantiate__has_correct_ordering(
      self,
      report_store_admin: ReportStoreAdmin,
  ) -> None:
    assert report_store_admin.ordering == ("store__franchise__name", "store")

  def test_instantiate__has_correct_search_fields(
      self,
      report_store_admin: ReportStoreAdmin,
  ) -> None:
    assert report_store_admin.search_fields == (
        "store__address__locality__name",
        "store__franchise__name",
    )
