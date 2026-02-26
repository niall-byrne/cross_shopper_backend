"""Shared query sets for the Reports API endpoints."""

from typing import TYPE_CHECKING

from items.models import Item
from scrapers.models import ScraperConfig

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet

REPORT_ITEM_ORDERING = (
    "name",
    "brand__name",
    "is_organic",
    "packaging__container",
    "packaging__quantity",
)


def qs_item() -> "QuerySet[Item]":
  """Generate the Item query set sorted for Report models."""
  return Item.objects.order_by(*REPORT_ITEM_ORDERING)


def qs_scraper_config() -> "QuerySet[ScraperConfig]":
  """Generate the ScraperConfig query set for Report models."""
  return ScraperConfig.objects.all()
