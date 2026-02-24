"""Admin for the error model."""

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from errors.admin import filters
from errors.models import Error
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)
from scrapers.models import ScraperConfig
from utilities.admin.list_display_column import (
    ColumnLinkConfig,
    ColumnObjectConfig,
    column_generator,
)


class ScraperConfigAdminActions(ScraperConfigActionsAdminMixin[ScraperConfig]):
  scraper_config_is_related_model = True


class ErrorAdmin(ScraperConfigAdminActions, admin.ModelAdmin[Error]):
  ordering = (
      "type__name",
      "store__franchise__name",
      "item__name",
      "scraper_config__url",
  )
  search_fields = (
      "store__franchise__name",
      "item__name",
      "scraper_config__url",
  )
  list_filter = filters.error_filter
  actions = (
      "mark_as_reoccurring",
      "mark_as_non_reoccurring",
      "activate_scraper_configs",
      "deactivate_scraper_configs",
  )
  list_display = (
      "error",
      "count",
      "is_reoccurring",
      "error_franchise",
      "error_item",
      "error_url",
      "error_store",
  )

  @admin.action(description="Mark selected errors as reoccurring")
  def mark_as_reoccurring(
      self,
      request: HttpRequest,
      queryset: QuerySet[Error],
  ):
    """Mark the selected errors as reoccurring."""
    updated_count = queryset.update(is_reoccurring=True)
    self.message_user(
        request,
        f"{updated_count} errors were successfully marked as reoccurring."
    )

  @admin.action(description="Mark selected errors as non-reoccurring")
  def mark_as_non_reoccurring(
      self,
      request: HttpRequest,
      queryset: QuerySet[Error],
  ):
    """Mark the selected errors as non-reoccurring."""
    updated_count = queryset.update(is_reoccurring=False)
    self.message_user(
        request,
        f"{updated_count} errors were successfully marked as non-reoccurring."
    )


column_generator(ErrorAdmin)(
    config=[
        ColumnObjectConfig(
            method_name="error",
            description="Error",
            obj_lookup="type",
        ),
        ColumnLinkConfig(
            method_name="error_item",
            description="Item",
            reverse_url_name="admin:items_item_change",
            obj_id_lookup="item.id",
            obj_name_lookup="item.full_name"
        ),
        ColumnLinkConfig(
            method_name="error_franchise",
            description="Franchise",
            reverse_url_name="admin:stores_franchise_change",
            obj_id_lookup="store.franchise.id",
            obj_name_lookup="store.franchise.name"
        ),
        ColumnLinkConfig(
            method_name="error_store",
            description="Store",
            reverse_url_name="admin:stores_store_change",
            obj_id_lookup="store.id",
            obj_name_lookup="store.address"
        ),
        ColumnLinkConfig(
            method_name="error_url",
            description="URL",
            reverse_url_name="admin:scrapers_scraperconfig_change",
            obj_id_lookup="scraper_config.id",
            obj_name_lookup="scraper_config.url"
        )
    ]
)
