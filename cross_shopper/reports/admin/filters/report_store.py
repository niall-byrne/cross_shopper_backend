"""ReportStore model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class ReportFilter(AdminListFilterBase):
  title = 'report'
  parameter_name = 'report__name'


class FranchiseFilter(AdminListFilterBase):
  title = 'franchise'
  parameter_name = 'store__franchise__name'


report_store_filter = (
    ReportFilter,
    FranchiseFilter,
    'report__is_testing_only',
)
