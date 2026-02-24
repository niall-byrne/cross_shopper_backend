"""Brand model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class BrandFilter(AdminListFilterBase):
  title = 'brand'
  parameter_name = 'item__brand__name'
