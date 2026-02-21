"""Test the admin for the ScraperConfig model."""

from django.contrib import admin
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)
from scrapers.admin.scraper_config import ScraperConfigAdmin


class TestScraperConfigAdmin:
  """Test the ScraperConfigAdmin class."""

  def test_instantiate__inheritance(
      self, scraper_config_admin: ScraperConfigAdmin
  ) -> None:
    assert isinstance(scraper_config_admin, admin.ModelAdmin)
    assert isinstance(scraper_config_admin, ScraperConfigActionsAdminMixin)

  def test_instantiate__ordering(
      self, scraper_config_admin: ScraperConfigAdmin
  ) -> None:
    assert scraper_config_admin.ordering == ('scraper__name', 'url')

  def test_instantiate__search_fields(
      self, scraper_config_admin: ScraperConfigAdmin
  ) -> None:
    assert scraper_config_admin.search_fields == ('scraper__name', 'url')

  def test_instantiate__actions(
      self, scraper_config_admin: ScraperConfigAdmin
  ) -> None:
    assert scraper_config_admin.actions == (
        "activate_scraper_configs",
        "deactivate_scraper_configs",
    )
