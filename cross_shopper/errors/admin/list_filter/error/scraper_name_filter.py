"""Scraper name model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class ScraperNameFilter(AdminListFilterBase):
  title = "scraper"
  parameter_name = "scraper_config__scraper__name"
