"""Admin models for the scrapers app."""

from django.contrib import admin
from scrapers.admin.scraper import ScraperAdmin
from scrapers.admin.scraper_config import ScraperConfigAdmin
from scrapers.models import Scraper, ScraperConfig

admin.site.register(Scraper, ScraperAdmin)
admin.site.register(
    ScraperConfig,
    ScraperConfigAdmin,
)
