"""Test the admin for the ItemScraperConfig model."""

from typing import TYPE_CHECKING

from django.contrib import admin
from items.admin.list_filters.item_scraper_config import (
    item_scraper_config_list_filter,
)
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)

if TYPE_CHECKING:  # no cover
  from items.admin.item_scraper_config import ItemScraperConfigAdmin


class TestItemScraperConfigAdmin:

  def test_instantiate__inheritance(
      self,
      item_scraper_config_admin: "ItemScraperConfigAdmin",
  ) -> None:
    assert isinstance(item_scraper_config_admin, admin.ModelAdmin)
    assert isinstance(item_scraper_config_admin, ScraperConfigActionsAdminMixin)

  def test_instantiate__has_correct_actions(
      self,
      item_scraper_config_admin: "ItemScraperConfigAdmin",
  ) -> None:
    assert item_scraper_config_admin.actions == (
        "action_activate_scraper_configs",
        "action_deactivate_scraper_configs",
    )

  def test_instantiate__has_correct_list_filter(
      self,
      item_scraper_config_admin: "ItemScraperConfigAdmin",
  ) -> None:
    assert item_scraper_config_admin.list_filter == (
        item_scraper_config_list_filter
    )

  def test_instantiate__has_correct_ordering(
      self,
      item_scraper_config_admin: "ItemScraperConfigAdmin",
  ) -> None:
    assert item_scraper_config_admin.ordering == (
        "item__name",
        "scraper_config__scraper__name",
        "scraper_config__url",
    )

  def test_instantiate__has_correct_search_fields(
      self,
      item_scraper_config_admin: "ItemScraperConfigAdmin",
  ) -> None:
    assert item_scraper_config_admin.search_fields == (
        "scraper_config__scraper__name",
        "scraper_config__url",
        "item__name",
    )
