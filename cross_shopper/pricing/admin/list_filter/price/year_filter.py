"""Year model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class YearFilter(AdminListFilterBase):
  title = 'year'
  parameter_name = 'year'
  is_reversed = True
