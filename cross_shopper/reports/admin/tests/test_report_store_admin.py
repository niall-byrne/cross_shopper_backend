"""Test the admin for the ReportStore model."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from reports.admin.report_store import ReportStoreAdmin


class TestReportStoreAdmin:

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
