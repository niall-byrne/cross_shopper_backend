"""Test the admin for the ItemScraperConfig model."""

from django.contrib import admin
from items.admin.list_filter.item_scraper_config import item_scraper_config_filter
from items.admin.item_scraper_config import ItemScraperConfigAdmin
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)


class TestItemScraperConfigAdmin:
  """Test the ItemScraperConfigAdmin class."""

  def test_instantiate__inheritance(
      self,
      item_scraper_config_admin: ItemScraperConfigAdmin,
  ) -> None:
    assert isinstance(item_scraper_config_admin, admin.ModelAdmin)
    assert isinstance(item_scraper_config_admin, ScraperConfigActionsAdminMixin)

  def test_instantiate__has_correct_actions(
      self,
      item_scraper_config_admin: ItemScraperConfigAdmin,
  ) -> None:
    assert item_scraper_config_admin.actions == (
        "activate_scraper_configs",
        "deactivate_scraper_configs",
    )

  def test_instantiate__has_correct_list_display(
      self,
      item_scraper_config_admin: ItemScraperConfigAdmin,
  ) -> None:
    assert item_scraper_config_admin.list_display == (
        "item_scraper_config",
        "item_scraper_config__scraper_config__is_active",
        'item_scraper_config__item',
        "item_scraper_config__scraper_config",
    )

  def test_instantiate__has_correct_list_filter(
      self,
      item_scraper_config_admin: ItemScraperConfigAdmin,
  ) -> None:
    assert item_scraper_config_admin.list_filter == item_scraper_config_filter

  def test_instantiate__has_correct_ordering(
      self,
      item_scraper_config_admin: ItemScraperConfigAdmin,
  ) -> None:
    assert item_scraper_config_admin.ordering == (
        'item__name',
        'scraper_config__scraper__name',
        'scraper_config__url',
    )

  def test_instantiate__has_correct_search_fields(
      self,
      item_scraper_config_admin: ItemScraperConfigAdmin,
  ) -> None:
    assert item_scraper_config_admin.search_fields == (
        'scraper_config__scraper__name',
        'scraper_config__url',
        'item__name',
    )
