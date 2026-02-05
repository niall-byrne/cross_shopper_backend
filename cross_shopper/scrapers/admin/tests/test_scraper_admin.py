"""Test the admin for the Scraper model."""

from django.contrib import admin
from scrapers.admin.scraper import ScraperAdmin


class TestScraperAdmin:
  """Test the ScraperAdmin class."""

  def test_instantiate__inheritance(
      self,
      scraper_admin: ScraperAdmin,
  ) -> None:
    assert isinstance(scraper_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_ordering(
      self,
      scraper_admin: ScraperAdmin,
  ) -> None:
    assert scraper_admin.ordering == ('name',)
