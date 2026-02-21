"""Error model list filter."""

from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)


class ErrorTypeFilter(AdminListFilterBase):
  title = "type"
  parameter_name = "type__name"


class FranchiseNameFilter(AdminListFilterBase):
  title = "franchise"
  parameter_name = "store__franchise__name"


class IsReoccurringFilter(AdminListFilterBase):
  title = "is_reoccurring"
  parameter_name = "is_reoccurring"


class ItemNameFilter(AdminListFilterBase):
  title = "item"
  parameter_name = "item__name"


class ScraperConfigIsActiveFilter(AdminListFilterBase):
  title = "scraper_config active"
  parameter_name = "scraper_config__is_active"


class ScraperNameFilter(AdminListFilterBase):
  title = "scraper"
  parameter_name = "scraper_config__scraper__name"


error_filter = (
    ErrorTypeFilter,
    ItemNameFilter,
    IsReoccurringFilter,
    FranchiseNameFilter,
    ScraperConfigIsActiveFilter,
    ScraperNameFilter,
)
