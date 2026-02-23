"""Test the ItemScraperConfig model."""

import pytest
from django.core.exceptions import ValidationError
from items.models import Item, ItemScraperConfig


@pytest.mark.django_db
class TestItemScraperConfig:

  def test_constraint__unique_together(
      self,
      item_scraper_config: ItemScraperConfig,
  ) -> None:
    item_scraper_config2 = ItemScraperConfig(
        item=item_scraper_config.item,
        scraper_config=item_scraper_config.scraper_config,
    )

    with pytest.raises(ValidationError) as exc:
      item_scraper_config2.save()

    assert str(exc.value) == str(
        {
            "__all__":
                [
                    "Item scraper config with this Item and Scraper config "
                    "already exists."
                ],
            "scraper_config":
                [
                    "Item scraper config with this Scraper config already "
                    "exists."
                ]
        }
    )

  def test_constraint__unique_scraper_config(
      self,
      item: Item,
      item_scraper_config: ItemScraperConfig,
  ) -> None:
    item_scraper_config2 = ItemScraperConfig(
        item=item,
        scraper_config=item_scraper_config.scraper_config,
    )

    with pytest.raises(ValidationError) as exc:
      item_scraper_config2.save()

    assert str(exc.value) == str(
        {
            "scraper_config":
                [
                    "Item scraper config with this Scraper config already "
                    "exists."
                ]
        }
    )

  def test_str__returns_str_of_scraper_config(
      self,
      item_scraper_config: ItemScraperConfig,
  ) -> None:
    assert str(item_scraper_config) == (
        f"{item_scraper_config.item.name} - "
        f"{item_scraper_config.scraper_config}"
    )
