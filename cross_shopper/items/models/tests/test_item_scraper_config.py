"""Test the ItemScraperConfig model."""

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:  # no cover
  from items.models import ItemScraperConfig


@pytest.mark.django_db
class TestItemScraperConfig:

  def test_str__returns_str_of_scraper_config(
      self,
      item_scraper_config: "ItemScraperConfig",
  ) -> None:
    assert str(item_scraper_config) == (
        f"{item_scraper_config.item.name} - "
        f"{item_scraper_config.scraper_config}"
    )
