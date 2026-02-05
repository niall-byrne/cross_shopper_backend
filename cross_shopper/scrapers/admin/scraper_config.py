"""Admin for the scraper config model."""

from django.contrib import admin
from scrapers.models import ScraperConfig


class ScraperConfigAdmin(admin.ModelAdmin[ScraperConfig]):
  ordering = ('scraper__name', 'url')
