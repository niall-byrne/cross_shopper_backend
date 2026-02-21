"""ScraperConfig model list filter."""

from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)


class ScraperFilter(AdminListFilterBase):
  title = 'scraper name'
  parameter_name = 'scraper__name'


scraper_config_filter = ("is_active", ScraperFilter)
