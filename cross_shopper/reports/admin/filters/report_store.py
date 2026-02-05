"""ReportStore model list filter."""

from utilities.admin.filters.bases.base_admin_list_filter import (
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
