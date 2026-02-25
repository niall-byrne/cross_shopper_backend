"""Test the admin for the ScraperConfig model."""

from django.contrib import admin
from scrapers.admin.list_filter.scraper_config import scraper_config_list_filter
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)
from scrapers.admin.scraper_config import ScraperConfigAdmin


class TestScraperConfigAdmin:
  """Test the ScraperConfigAdmin class."""

  def test_instantiate__inheritance(
      self,
      scraper_config_admin: ScraperConfigAdmin,
  ) -> None:
    assert isinstance(scraper_config_admin, admin.ModelAdmin)
    assert isinstance(scraper_config_admin, ScraperConfigActionsAdminMixin)

  def test_instantiate__has_correct_actions(
      self,
      scraper_config_admin: ScraperConfigAdmin,
  ) -> None:
    assert scraper_config_admin.actions == (
        "activate_scraper_configs",
        "deactivate_scraper_configs",
    )

  def test_instantiate__has_correct_list_display(
      self,
      scraper_config_admin: ScraperConfigAdmin,
  ) -> None:
    assert scraper_config_admin.list_display == (
        'scraper_config__url',
        'is_active',
        'scraper_config__scraper__name',
        'scraper_config__has_item',
        'scraper_config__associated_item',
    )

  def test_instantiate__has_correct_list_filter(
      self,
      scraper_config_admin: ScraperConfigAdmin,
  ) -> None:
    assert scraper_config_admin.list_filter == scraper_config_list_filter

  def test_instantiate__has_correct_ordering(
      self,
      scraper_config_admin: ScraperConfigAdmin,
  ) -> None:
    assert scraper_config_admin.ordering == ('scraper__name', 'url')

  def test_instantiate__has_correct_search_fields(
      self, scraper_config_admin: ScraperConfigAdmin
  ) -> None:
    assert scraper_config_admin.search_fields == ('scraper__name', 'url')
