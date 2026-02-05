"""Store model list filter."""

from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)


class FranchiseFilter(AdminListFilterBase):
  title = 'franchise'
  parameter_name = 'franchise__name'


class LocationFilter(AdminListFilterBase):
  title = 'location'
  parameter_name = 'address__locality__name'


store_filter = (FranchiseFilter, LocationFilter)
