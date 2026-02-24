"""Error type model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class ErrorTypeFilter(AdminListFilterBase):
  title = "type"
  parameter_name = "type__name"
