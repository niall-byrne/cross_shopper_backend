"""Item admin model ItemScraperConfig inline."""

from django.contrib import admin
from items.models import Item, ItemScraperConfig


class ItemScraperConfigInline(
    admin.StackedInline[ItemScraperConfig, Item],
):
  extra = 0
  ordering = (
      'scraper_config__scraper__name',
      'scraper_config__url',
  )
  model = ItemScraperConfig
  verbose_name = 'Scraper Configuration'
  verbose_name_plural = 'Scraper Configurations'
