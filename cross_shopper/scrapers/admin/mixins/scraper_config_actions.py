"""An admin mixin class providing ScraperConfig model actions."""

from typing import TYPE_CHECKING, Generic, cast

from django.contrib import admin
from scrapers.models import ScraperConfig
from .types import AdminMixinType, ModelType

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet
  from django.http import HttpRequest


class ScraperConfigActionsAdminMixin(
    Generic[ModelType],
):
  """An admin mixin class providing ScraperConfig model actions."""

  scraper_config_is_related_model = False

  def _as_mixin(self) -> "AdminMixinType":
    return cast("AdminMixinType", self)

  def _get_model_name(self) -> str:
    if self.scraper_config_is_related_model:
      return "related scraper configs"
    return "scraper configs"

  def _get_query_set(
      self,
      admin_queryset: "QuerySet[ModelType]",
  ) -> "QuerySet[ScraperConfig]":
    if self.scraper_config_is_related_model:
      scraper_config_ids = admin_queryset.values_list(
          "scraper_config__id", flat=True
      )
      return ScraperConfig.objects.filter(id__in=scraper_config_ids)
    else:
      return cast("QuerySet[ScraperConfig]", admin_queryset)

  @admin.action(  # type: ignore[type-var]
    description="Activate scraper configs"
  )
  def action_activate_scraper_configs(
      self,
      request: "HttpRequest",
      admin_queryset: "QuerySet[ModelType]",
  ) -> None:
    """Activate the selected scraper configs."""
    updated_count = self._get_query_set(admin_queryset).update(is_active=True)

    self._as_mixin().message_user(
        request,
        f"{updated_count} {self._get_model_name()} were successfully activated."
    )

  @admin.action(  # type: ignore[type-var]
    description="Deactivate scraper configs"
  )
  def action_deactivate_scraper_configs(
      self,
      request: "HttpRequest",
      admin_queryset: "QuerySet[ModelType]",
  ) -> None:
    """Disable the selected scraper configs."""
    updated_count = self._get_query_set(admin_queryset).update(is_active=False)

    self._as_mixin().message_user(
        request,
        f"{updated_count} {self._get_model_name()} were successfully deactivated.",
    )
