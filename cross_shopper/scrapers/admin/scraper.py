"""Admin for the scraper model."""

from django.contrib import admin
from scrapers.models import Scraper


class ScraperAdmin(admin.ModelAdmin[Scraper]):
  ordering = ("name",)
