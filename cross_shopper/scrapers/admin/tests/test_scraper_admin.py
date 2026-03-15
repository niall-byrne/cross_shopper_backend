"""Test the admin for the Scraper model."""

from typing import TYPE_CHECKING

from django.contrib import admin

if TYPE_CHECKING:  # no cover
  from scrapers.admin.scraper import ScraperAdmin


class TestScraperAdmin:

  def test_instantiate__inheritance(
      self,
      scraper_admin: 'ScraperAdmin',
  ) -> None:
    assert isinstance(scraper_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_ordering(
      self,
      scraper_admin: 'ScraperAdmin',
  ) -> None:
    assert scraper_admin.ordering == ('name',)
