"""ScraperConfig model list filter."""

from typing import TYPE_CHECKING

from items.models import ItemScraperConfig
from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)

if TYPE_CHECKING:  # no cover
  from django.db import models
  from django.http import HttpRequest
  from scrapers.models import ScraperConfig


class ScraperFilter(AdminListFilterBase):
  title = 'scraper name'
  parameter_name = 'scraper__name'


class HasItemsFilter(AdminListFilterBase):
  title = 'has items'
  parameter_name = 'has_item'
  is_boolean = True

  def queryset(
      self,
      request: "HttpRequest",
      queryset: "models.QuerySet[ScraperConfig]",
  ) -> "models.QuerySet[ScraperConfig]":
    """Generate a list of filter tuples from the configured query set."""
    if self.value() == 'True':
      return ItemScraperConfig.associations.with_items(queryset)
    if self.value() == 'False':
      return ItemScraperConfig.associations.with_no_items(queryset)
    return queryset


scraper_config_filter = ("is_active", ScraperFilter, HasItemsFilter)
