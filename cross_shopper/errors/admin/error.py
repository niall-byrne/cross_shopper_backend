"""Admin for the error model."""

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from errors.models import Error
from scrapers.models import ScraperConfig


class ErrorAdmin(admin.ModelAdmin[Error]):
  ordering = (
      "-count",
      "type",
      "store__franchise__name",
      "item__name",
      "scraper_config",
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

  @admin.action(description="Activate related scraper configs")
  def activate_scraper_configs(
      self,
      request: HttpRequest,
      queryset: QuerySet[Error],
  ):
    """Activate the selected scraper configs."""
    scraper_config_ids = queryset.values_list('scraper_config__id', flat=True)
    scraper_config_queryset = ScraperConfig.objects.filter(
        id__in=scraper_config_ids
    )
    updated_count = scraper_config_queryset.update(is_active=True)

    self.message_user(
        request, f"{updated_count} related scraper configs were successfully "
        "activated."
    )

  @admin.action(description="Deactivate related scraper configs")
  def deactivate_scraper_configs(
      self,
      request: HttpRequest,
      queryset: QuerySet[Error],
  ):
    """Disable the selected scraper configs."""
    scraper_config_ids = queryset.values_list('scraper_config__id', flat=True)
    scraper_config_queryset = ScraperConfig.objects.filter(
        id__in=scraper_config_ids
    )
    updated_count = scraper_config_queryset.update(is_active=False)

    self.message_user(
        request, f"{updated_count} related scraper configs were successfully "
        "deactivated."
    )
