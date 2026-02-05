"""Admin models for the scrapers app."""

from django.contrib import admin
from ..models import Scraper, ScraperConfig
from . import filters
from .scraper import ScraperAdmin
from .scraper_config import ScraperConfigAdmin

admin.site.register(Scraper, ScraperAdmin)
admin.site.register(
    ScraperConfig,
    ScraperConfigAdmin,
    list_filter=filters.scraper_config_filter,
)
