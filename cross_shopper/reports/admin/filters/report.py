"""Report model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class ItemFilter(AdminListFilterBase):
  title = 'item'
  parameter_name = 'item__name'


class FranchiseFilter(AdminListFilterBase):
  title = 'franchise'
  parameter_name = 'store__franchise__name'


class LocationFilter(AdminListFilterBase):
  title = 'location'
  parameter_name = 'store__address__locality__name'


report_filter = (
    ItemFilter,
    FranchiseFilter,
    LocationFilter,
    'is_testing_only',
)
