"""Test the admin for the ScraperConfig model."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from scrapers.admin.list_filters.scraper_config import (
    scraper_config_list_filter,
)

if TYPE_CHECKING:
  from scrapers.admin.scraper_config import ScraperConfigAdmin


class TestScraperConfigAdmin:

  def test_instantiate__inheritance(
      self,
      scraper_config_admin: ScraperConfigAdmin,
  ) -> None:
    assert isinstance(scraper_config_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_list_filter(
      self,
      scraper_config_admin: ScraperConfigAdmin,
  ) -> None:
    assert scraper_config_admin.list_filter == scraper_config_list_filter

  def test_instantiate__has_correct_ordering(
      self,
      scraper_config_admin: ScraperConfigAdmin,
  ) -> None:
    assert scraper_config_admin.ordering == ("scraper__name", "url")
