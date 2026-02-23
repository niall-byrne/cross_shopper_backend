"""ScraperConfig model list filter."""

from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)


class ItemFilter(AdminListFilterBase):
  title = 'item name'
  parameter_name = 'item__name'


class ScraperFilter(AdminListFilterBase):
  title = 'scraper name'
  parameter_name = 'scraper_config__scraper__name'


class ScraperIsActiveFilter(AdminListFilterBase):
  title = 'is active'
  parameter_name = 'scraper_config__is_active'
  is_boolean = True


item_scraper_config_filter = (ScraperIsActiveFilter, ScraperFilter, ItemFilter)
