"""ScraperConfig model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class ScraperFilter(AdminListFilterBase):
  title = 'scraper'
  parameter_name = 'scraper__name'


scraper_config_filter = (ScraperFilter,)
