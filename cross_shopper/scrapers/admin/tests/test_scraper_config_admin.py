"""Test the admin for the ScraperConfig model."""

from django.contrib import admin
from scrapers.admin.scraper_config import ScraperConfigAdmin


class TestScraperConfigAdmin:
  """Test the ScraperConfigAdmin class."""

  def test_instantiate__inheritance(
      self, scraper_config_admin: ScraperConfigAdmin
  ) -> None:
    assert isinstance(scraper_config_admin, admin.ModelAdmin)

  def test_instantiate__ordering(
      self, scraper_config_admin: ScraperConfigAdmin
  ) -> None:
    assert scraper_config_admin.ordering == ('scraper__name', 'url')
