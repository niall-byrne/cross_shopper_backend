"""Report model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class ReportFilter(AdminListFilterBase):
  title = 'report'
  parameter_name = 'report__name'
