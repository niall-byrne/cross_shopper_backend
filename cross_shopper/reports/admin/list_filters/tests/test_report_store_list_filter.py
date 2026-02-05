"""Test the ReportStore admin model list filter."""

from reports.admin.list_filters.report_store import report_store_list_filter
from utilities.admin.list_filters import GenericListFilter
from utilities.testing.comparisons.is_subclass import DynamicSubClass


class TestReportStoreAdminListFilter:

  def test_list_filter(self) -> None:
    assert report_store_list_filter == (
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": 'report',
                "parameter_name": 'report__name',
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": 'franchise',
                "parameter_name": 'store__franchise__name',
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": 'location',
                "parameter_name": 'store__address__locality__name',
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
    )
