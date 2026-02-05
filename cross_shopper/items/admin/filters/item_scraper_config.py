"""ScraperConfig model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class ItemFilter(AdminListFilterBase):
  title = 'Item Name'
  parameter_name = 'item__name'


class ScraperFilter(AdminListFilterBase):
  title = 'Scraper Name'
  parameter_name = 'scraper_config__scraper__name'


item_scraper_config_filter = (ItemFilter, ScraperFilter)
