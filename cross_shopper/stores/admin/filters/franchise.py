"""Franchise model list filter."""

from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)


class ScraperFilter(AdminListFilterBase):
  title = 'scraper'
  parameter_name = 'scraper__name'


franchise_filter = (ScraperFilter,)
