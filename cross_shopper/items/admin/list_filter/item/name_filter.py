"""Name model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class NameFilter(AdminListFilterBase):
  title = 'name'
  parameter_name = 'name'
