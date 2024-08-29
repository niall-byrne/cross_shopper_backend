"""Admin models for the scrapers app."""

from django.contrib import admin
from scrapers.models import Scraper, ScraperConfig

admin.site.register(Scraper)
admin.site.register(ScraperConfig)
