"""Test the ItemScraperConfig model."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
  from items.models import ItemScraperConfig


@pytest.mark.django_db
class TestItemScraperConfig:

  def test_str__returns_str_of_scraper_config(
      self,
      item_scraper_config: ItemScraperConfig,
  ) -> None:
    assert str(item_scraper_config) == (
        f"{item_scraper_config.item.name} - "
        f"{item_scraper_config.scraper_config}"
    )
