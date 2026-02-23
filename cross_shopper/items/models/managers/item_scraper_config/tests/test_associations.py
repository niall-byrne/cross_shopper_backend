"""Test the Assocations model manager for the ItemScraperConfig model."""

from typing import TYPE_CHECKING

import pytest
from items.models import ItemScraperConfig
from scrapers.models import ScraperConfig

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet


@pytest.mark.django_db
class TestItemScraperConfig:

  def test_get_item__has_associated_item__returns_item(
      self,
      item_scraper_config: ItemScraperConfig,
  ) -> None:
    obj = ItemScraperConfig.associations.get_item(
        item_scraper_config.scraper_config
    )

    assert obj == item_scraper_config.item

  def test_get_item__no_associated_item__returns_none(
      self,
      item_scraper_config: ItemScraperConfig,
      scraper_config: ScraperConfig,
  ) -> None:
    obj = ItemScraperConfig.associations.get_item(scraper_config)

    assert obj is None

  def test_get_items__has_associated_items__returns_items(
      self,
      item_scraper_config_batch: "QuerySet[ItemScraperConfig]",
  ) -> None:
    scraper_config_ids = item_scraper_config_batch.values_list(
        "scraper_config__id",
        flat=True,
    )
    item_ids = item_scraper_config_batch.values_list(
        "item__id",
        flat=True,
    )
    scraper_configs = ScraperConfig.objects.filter(id__in=scraper_config_ids)

    qs = ItemScraperConfig.associations.get_items(scraper_configs)

    assert list(qs.values_list("id", flat=True)) == list(item_ids)

  def test_get_items__no_associated_items__returns_empty_list(
      self,
      scraper_config_batch: "QuerySet[ScraperConfig]",
  ) -> None:
    qs = ItemScraperConfig.associations.get_items(scraper_config_batch)

    assert list(qs) == []

  @pytest.mark.usefixtures("scraper_config")
  def test_with_items__returns_correct_scraper_configs(
      self,
      item_scraper_config_batch: "QuerySet[ItemScraperConfig]",
  ) -> None:
    scraper_config_ids = item_scraper_config_batch.values_list(
        "scraper_config__id",
        flat=True,
    )
    scraper_configs = ScraperConfig.objects.filter(id__in=scraper_config_ids)
    qs = ItemScraperConfig.associations.with_items(ScraperConfig.objects.all())

    assert list(qs) == list(scraper_configs)

  @pytest.mark.usefixtures("item_scraper_config_batch")
  def test_with_no_items__returns_correct_scraper_configs(
      self,
      scraper_config: "ScraperConfig",
  ) -> None:
    qs = ItemScraperConfig.associations.with_no_items(
        ScraperConfig.objects.all()
    )

    assert list(qs) == list(ScraperConfig.objects.filter(id=scraper_config.pk))
