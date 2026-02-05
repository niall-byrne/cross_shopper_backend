"""ScraperConfig model list filter."""

from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)


class ItemFilter(AdminListFilterBase):
  title = 'Item Name'
  parameter_name = 'item__name'


class ScraperFilter(AdminListFilterBase):
  title = 'Scraper Name'
  parameter_name = 'scraper_config__scraper__name'


scraper_config_filter = (ItemFilter, ScraperFilter)
