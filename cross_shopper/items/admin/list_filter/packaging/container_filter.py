"""Container model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class ContainerFilter(AdminListFilterBase):
  title = 'container name'
  parameter_name = 'container__name'
