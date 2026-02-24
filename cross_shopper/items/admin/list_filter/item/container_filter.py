"""Container model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class ContainerFilter(AdminListFilterBase):
  title = 'packaging'
  parameter_name = 'packaging__container__name'
