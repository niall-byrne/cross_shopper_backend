"""Item model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class ContainerFilter(AdminListFilterBase):
  title = 'packaging'
  parameter_name = 'packaging__container__name'


class BrandFilter(AdminListFilterBase):
  title = 'brand'
  parameter_name = 'brand__name'


class NameFilter(AdminListFilterBase):
  title = 'name'
  parameter_name = 'name'


item_filter = (
    'is_non_gmo',
    'is_organic',
    BrandFilter,
    ContainerFilter,
    NameFilter,
)
