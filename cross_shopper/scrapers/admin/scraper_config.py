"""Admin for the scraper config model."""

from typing import TYPE_CHECKING

from django.contrib import admin
from scrapers.admin.list_filters.scraper_config import (
    scraper_config_list_filter,
)
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)

if TYPE_CHECKING:  # no cover
  from scrapers.models import ScraperConfig  # noqa: F401


class ScraperConfigAdmin(
    ScraperConfigActionsAdminMixin["ScraperConfig"],
    admin.ModelAdmin["ScraperConfig"]
):
  scraper_config_is_related_model = False

  actions = (
      "action_activate_scraper_configs",
      "action_deactivate_scraper_configs",
  )
  list_filter = scraper_config_list_filter
  ordering = ('scraper__name', 'url')
  search_fields = ('scraper__name', 'url')
