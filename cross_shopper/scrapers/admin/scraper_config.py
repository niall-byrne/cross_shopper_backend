"""Admin for the scraper config model."""

from typing import TYPE_CHECKING

from django.contrib import admin
from scrapers.admin.filters.scraper_config import scraper_config_filter

if TYPE_CHECKING:  # no cover
  from scrapers.models import ScraperConfig  # noqa: F401


class ScraperConfigAdmin(admin.ModelAdmin["ScraperConfig"]):
  list_filter = scraper_config_filter
  ordering = ('scraper__name', 'url')
