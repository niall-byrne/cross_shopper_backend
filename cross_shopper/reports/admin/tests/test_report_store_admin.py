"""Test the admin for the ReportStore model."""

from reports.admin.report_store import ReportStoreAdmin


class TestReportStoreAdmin:

  def test_instantiate__has_correct_ordering(
      self,
      report_store_admin: ReportStoreAdmin,
  ) -> None:
    assert report_store_admin.ordering == ("store__franchise__name", "store")
