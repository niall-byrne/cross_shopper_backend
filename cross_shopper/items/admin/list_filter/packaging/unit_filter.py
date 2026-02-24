"""Unit model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class UnitFilter(AdminListFilterBase):
  title = 'unit name'
  parameter_name = 'unit__name'
