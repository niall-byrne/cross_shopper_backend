"""Admin for the error model."""

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from errors.models import Error
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)
from scrapers.models import ScraperConfig


class ScraperConfigAdminActions(ScraperConfigActionsAdminMixin[ScraperConfig]):
  scraper_config_is_related_model = True


class ErrorAdmin(ScraperConfigAdminActions, admin.ModelAdmin[Error]):
  ordering = (
      "-count",
      "type",
      "store__franchise__name",
      "item__name",
      "scraper_config",
  )
  search_fields = (
      "store__franchise__name",
      "item__name",
      "scraper_config__url",
  )
  actions = (
      "mark_as_reoccurring",
      "mark_as_non_reoccurring",
      "activate_scraper_configs",
      "deactivate_scraper_configs",
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
