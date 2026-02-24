"""Test the report store model list filters."""

from reports.admin.filters.report_store import (
    FranchiseFilter,
    ReportFilter,
)
from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)


class TestReportFilter:
  """Test the ReportFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ReportFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ReportFilter.title == 'report'
    assert ReportFilter.parameter_name == 'report__name'


class TestFranchiseFilter:
  """Test the FranchiseFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(FranchiseFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert FranchiseFilter.title == 'franchise'
    assert FranchiseFilter.parameter_name == 'store__franchise__name'
