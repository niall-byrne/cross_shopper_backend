"""Test the admin for the ReportStore model."""

from reports.admin import ReportStoreAdmin


class TestReportStoreAdmin:
  """Test the ReportStoreAdmin class."""

  def test_instantiate__has_correct_search_fields(
      self,
      report_store_admin: ReportStoreAdmin,
  ) -> None:
    assert report_store_admin.search_fields == (
        "store__address__locality__name",
        "store__franchise__name",
    )
