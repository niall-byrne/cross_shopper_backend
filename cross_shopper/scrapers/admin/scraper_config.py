"""Admin for the scraper config model."""

from django.contrib import admin
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)
from scrapers.models import ScraperConfig

from . import filters
from utilities.admin.list_display_column import (
    ColumnLinkConfig,
    ColumnObjectConfig,
    column_generator,
)


class ScraperConfigAdminActions(ScraperConfigActionsAdminMixin[ScraperConfig]):
  scraper_config_is_related_model = False


class ScraperConfigAdmin(
    ScraperConfigAdminActions,
    admin.ModelAdmin[ScraperConfig],
):
  ordering = ('scraper__name', 'url')
  search_fields = ('scraper__name', 'url')
  actions = ("activate_scraper_configs", "deactivate_scraper_configs")
  list_filter = filters.scraper_config_filter
  list_display = (
      'scraper_config__url', 
      'is_active', 
      'scraper_config__scraper__name',
      'scraper_config__has_item',
      'scraper_config__associated_item',
  )


column_generator(ScraperConfigAdmin)(
    config=[
        ColumnObjectConfig(
            method_name="scraper_config__url",
            description="Scraper Config",
            obj_lookup="url",
        ),
        ColumnLinkConfig(
            method_name="scraper_config__scraper__name",
            description="Scraper",
            reverse_url_name="admin:scrapers_scraper_change",
            obj_id_lookup="scraper.id",
            obj_name_lookup="scraper.name",
        ),
        ColumnObjectConfig(
            method_name="scraper_config__has_item",
            description="Has Item",
            obj_lookup="has_item",
            is_boolean=True
        ),
        ColumnLinkConfig(
            method_name="scraper_config__associated_item",
            description="Associated Item",
            reverse_url_name="admin:items_item_change",
            obj_id_lookup="associated_item.id",
            obj_name_lookup="associated_item",
        )
    ]
)
