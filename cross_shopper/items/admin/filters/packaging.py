"""Packaging model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class ContainerFilter(AdminListFilterBase):
  title = 'container name'
  parameter_name = 'container__name'


class UnitFilter(AdminListFilterBase):
  title = 'unit name'
  parameter_name = 'unit__name'


packaging_filter = (ContainerFilter, UnitFilter)
