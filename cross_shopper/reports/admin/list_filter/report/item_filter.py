"""Item model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class ItemFilter(AdminListFilterBase):
  title = 'item'
  parameter_name = 'item__name'
