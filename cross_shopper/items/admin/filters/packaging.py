"""Packaging model list filter."""

from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)


class ContainerFilter(AdminListFilterBase):
  title = 'container name'
  parameter_name = 'container__name'


class UnitFilter(AdminListFilterBase):
  title = 'unit name'
  parameter_name = 'unit__name'


packaging_filter = (ContainerFilter, UnitFilter)
