"""Admin for the scraper config model."""

from django.contrib import admin
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)
from scrapers.models import ScraperConfig


class ScraperConfigAdminActions(ScraperConfigActionsAdminMixin[ScraperConfig]):
  scraper_config_is_related_model = False


class ScraperConfigAdmin(
    ScraperConfigAdminActions, admin.ModelAdmin[ScraperConfig]
):
  ordering = ('scraper__name', 'url')
  search_fields = ('scraper__name', 'url')
  actions = ("activate_scraper_configs", "deactivate_scraper_configs")
