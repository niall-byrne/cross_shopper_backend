"""Franchise model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class ScraperFilter(AdminListFilterBase):
  title = 'scraper'
  parameter_name = 'scraper__name'


franchise_filter = (ScraperFilter,)
