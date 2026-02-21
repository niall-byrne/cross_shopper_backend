"""Admin for the error model."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from errors.admin.list_filters.error import error_list_filter
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)

if TYPE_CHECKING:
  from django.db.models import QuerySet
  from django.http import HttpRequest
  from errors.models import Error


class ErrorAdmin(
    ScraperConfigActionsAdminMixin["Error"],
    admin.ModelAdmin["Error"],
):
  scraper_config_is_related_model = True

  actions = (
      "action_activate_scraper_configs",
      "action_deactivate_scraper_configs",
      "action_mark_as_reoccurring",
      "action_mark_as_non_reoccurring",
      "action_reset_error_count",
  )
  list_filter = error_list_filter
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

  @admin.action(description="Mark selected errors as reoccurring")
  def action_mark_as_reoccurring(
      self,
      request: HttpRequest,
      queryset: QuerySet[Error],
  ) -> None:
    """Mark the selected errors as reoccurring."""
    updated_count = queryset.update(is_reoccurring=True)
    self.message_user(
        request,
        f"{updated_count} errors were successfully marked as reoccurring."
    )

  @admin.action(description="Mark selected errors as non-reoccurring")
  def action_mark_as_non_reoccurring(
      self,
      request: HttpRequest,
      queryset: QuerySet[Error],
  ) -> None:
    """Mark the selected errors as non-reoccurring."""
    updated_count = queryset.update(is_reoccurring=False)
    self.message_user(
        request,
        f"{updated_count} errors were successfully marked as non-reoccurring."
    )

  @admin.action(description="Reset error count")
  def action_reset_error_count(
      self,
      request: HttpRequest,
      queryset: QuerySet[Error],
  ) -> None:
    """Reset the selected error counts."""
    updated_count = queryset.update(count=0)
    self.message_user(
        request, f"{updated_count} error counts were successfully reset."
    )
