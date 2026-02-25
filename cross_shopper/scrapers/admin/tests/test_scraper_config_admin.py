"""Test the admin for the ScraperConfig model."""

from typing import TYPE_CHECKING

from django.contrib import admin
from scrapers.admin.list_displays.scraper_config import (
    scraper_config_list_display,
)
from scrapers.admin.list_filters.scraper_config import (
    scraper_config_list_filter,
)
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)

if TYPE_CHECKING:  # no cover
  from scrapers.admin.scraper_config import ScraperConfigAdmin


class TestScraperConfigAdmin:

  def test_instantiate__inheritance(
      self,
      scraper_config_admin: "ScraperConfigAdmin",
  ) -> None:
    assert isinstance(scraper_config_admin, admin.ModelAdmin)
    assert isinstance(scraper_config_admin, ScraperConfigActionsAdminMixin)

  def test_instantiate__has_correct_actions(
      self,
      scraper_config_admin: "ScraperConfigAdmin",
  ) -> None:
    assert scraper_config_admin.actions == (
        "action_activate_scraper_configs",
        "action_deactivate_scraper_configs",
    )

  def test_instantiate__has_correct_list_display(
      self,
      scraper_config_admin: "ScraperConfigAdmin",
  ) -> None:
    assert scraper_config_admin.list_display == tuple(
        map(str, scraper_config_list_display)
    )

  def test_instantiate__has_correct_list_filter(
      self,
      scraper_config_admin: "ScraperConfigAdmin",
  ) -> None:
    assert scraper_config_admin.list_filter == scraper_config_list_filter

  def test_instantiate__has_correct_ordering(
      self,
      scraper_config_admin: "ScraperConfigAdmin",
  ) -> None:
    assert scraper_config_admin.ordering == ("scraper__name", "url")

  def test_instantiate__has_correct_search_fields(
      self, scraper_config_admin: "ScraperConfigAdmin"
  ) -> None:
    assert scraper_config_admin.search_fields == ("scraper__name", "url")
