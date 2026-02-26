"""Test the Report admin model list filter."""

from reports.admin.list_filter.report import report_list_filter
from utilities.admin.list_filter import GenericListFilter
from utilities.testing.comparisons.is_subclass import DynamicSubClass


class TestReportAdminListFilter:

  def test_list_filter(self) -> None:
    assert report_list_filter == (
        'is_testing',
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": 'has franchise',
                "parameter_name": 'store__franchise__name',
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": 'has store in',
                "parameter_name": 'store__address__locality__name',
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
    )
