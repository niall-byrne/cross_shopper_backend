"""Location model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class LocationFilter(AdminListFilterBase):
  title = 'location'
  parameter_name = 'address__locality__name'
