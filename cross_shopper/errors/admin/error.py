"""Admin for the error model."""

from typing import TYPE_CHECKING

from django.contrib import admin
from errors.admin.filters.error import error_filter
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet
  from django.http import HttpRequest
  from errors.models import Error


class ErrorAdmin(
    ScraperConfigActionsAdminMixin["Error"],
    admin.ModelAdmin["Error"],
):
  scraper_config_is_related_model = True

  actions = (
      "mark_as_reoccurring",
      "mark_as_non_reoccurring",
      "activate_scraper_configs",
      "deactivate_scraper_configs",
  )
  list_filter = error_filter
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

  @admin.action(description="Mark selected errors as reoccurring")
  def mark_as_reoccurring(
      self,
      request: "HttpRequest",
      queryset: "QuerySet[Error]",
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
      request: "HttpRequest",
      queryset: "QuerySet[Error]",
  ):
    """Mark the selected errors as non-reoccurring."""
    updated_count = queryset.update(is_reoccurring=False)
    self.message_user(
        request,
        f"{updated_count} errors were successfully marked as non-reoccurring."
    )
