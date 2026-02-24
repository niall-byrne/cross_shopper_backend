"""Scraper config is active model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class ScraperConfigIsActiveFilter(AdminListFilterBase):
  title = "scraper_config active"
  parameter_name = "scraper_config__is_active"
  is_boolean = True
