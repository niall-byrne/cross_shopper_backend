"""Test the ItemScraperConfig admin model inline."""

from typing import TYPE_CHECKING

from django.contrib import admin
from items.models.item_scraper_config import ItemScraperConfig

if TYPE_CHECKING:  # no cover
  from items.admin.inlines.item.item_scraper_config import (
      ItemScraperConfigInline,
  )


class TestItemScraperConfigInline:

  def test_instantiate__inheritance(
      self,
      item_scraper_config_inline: "ItemScraperConfigInline",
  ) -> None:
    assert isinstance(item_scraper_config_inline, admin.StackedInline)

  def test_instantiate__has_correct_extra(
      self,
      item_scraper_config_inline: "ItemScraperConfigInline",
  ) -> None:
    assert item_scraper_config_inline.extra == 0

  def test_instantiate__has_correct_ordering(
      self,
      item_scraper_config_inline: "ItemScraperConfigInline",
  ) -> None:
    assert item_scraper_config_inline.ordering == (
        "scraper_config__scraper__name",
        "scraper_config__url",
    )

  def test_instantiate__has_correct_model(
      self,
      item_scraper_config_inline: "ItemScraperConfigInline",
  ) -> None:
    assert item_scraper_config_inline.model == ItemScraperConfig

  def test_instantiate__has_correct_verbose_name(
      self,
      item_scraper_config_inline: "ItemScraperConfigInline",
  ) -> None:
    assert item_scraper_config_inline.verbose_name == "Scraper Configuration"

  def test_instantiate__has_correct_verbose_name_plural(
      self,
      item_scraper_config_inline: "ItemScraperConfigInline",
  ) -> None:
    assert item_scraper_config_inline.verbose_name_plural == (
        "Scraper Configurations"
    )
