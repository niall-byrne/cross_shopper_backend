"""Test the ItemScraperConfig model."""

import pytest
from items.models import ItemScraperConfig


@pytest.mark.django_db
class TestItemScraperConfig:

  def test_str__returns_str_of_scraper_config(
      self,
      item_scraper_config: ItemScraperConfig,
  ) -> None:
    assert str(item_scraper_config) == str(item_scraper_config.scraper_config)
