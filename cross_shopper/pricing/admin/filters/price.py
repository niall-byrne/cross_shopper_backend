"""Admin model list filters for the pricing app."""

from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)


class ItemFilter(AdminListFilterBase):
  title = 'item'
  parameter_name = 'item__name'


class BrandFilter(AdminListFilterBase):
  title = 'brand'
  parameter_name = 'item__brand__name'


class FranchiseFilter(AdminListFilterBase):
  title = 'franchise'
  parameter_name = 'store__franchise__name'


class LocationFilter(AdminListFilterBase):
  title = 'location'
  parameter_name = 'store__address__locality__name'


class YearFilter(AdminListFilterBase):
  title = 'year'
  parameter_name = 'year'
  reverse = True


price_filter = (
    ItemFilter,
    BrandFilter,
    FranchiseFilter,
    LocationFilter,
    YearFilter,
    'week',
)
