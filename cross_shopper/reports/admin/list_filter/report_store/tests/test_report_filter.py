"""Test the ReportFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from reports.admin.list_filter.report_store.report_filter import ReportFilter


@pytest.mark.django_db
class TestReportFilter:
  """Test the ReportFilter class."""

  def test_inheritance(self) -> None:
    """Test that ReportFilter inherits from AdminListFilterBase."""
    assert issubclass(ReportFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    """Test the ReportFilter attributes."""
    assert ReportFilter.title == 'report'
    assert ReportFilter.parameter_name == 'report__name'
