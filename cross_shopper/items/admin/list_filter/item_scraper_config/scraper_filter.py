"""Scraper model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class ScraperFilter(AdminListFilterBase):
  title = 'scraper name'
  parameter_name = 'scraper_config__scraper__name'
