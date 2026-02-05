"""Store model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class FranchiseFilter(AdminListFilterBase):
  title = 'franchise'
  parameter_name = 'franchise__name'


class LocationFilter(AdminListFilterBase):
  title = 'location'
  parameter_name = 'address__locality__name'


store_filter = (FranchiseFilter, LocationFilter)
