"""Test the admin for the ItemScraperConfig model."""

from django.contrib import admin
from items.admin.item_scraper_config import ItemScraperConfigAdmin
from items.admin.list_filters.item_scraper_config import (
    item_scraper_config_list_filter,
)


class TestItemScraperConfigAdmin:

  def test_instantiate__inheritance(
      self,
      item_scraper_config_admin: ItemScraperConfigAdmin,
  ) -> None:
    assert isinstance(item_scraper_config_admin, admin.ModelAdmin)

  def test_instantiate__has_list_filter(
      self,
      item_scraper_config_admin: ItemScraperConfigAdmin,
  ) -> None:
    assert item_scraper_config_admin.list_filter == (
        item_scraper_config_list_filter
    )

  def test_instantiate__has_correct_ordering(
      self,
      item_scraper_config_admin: ItemScraperConfigAdmin,
  ) -> None:
    assert item_scraper_config_admin.ordering == (
        "item__name",
        "scraper_config__scraper__name",
        "scraper_config__url",
    )
