"""Test the ScraperConfig model."""

import pytest
from django.core.exceptions import ValidationError
from items.models import ItemScraperConfig
from scrapers.models import Scraper, ScraperConfig


@pytest.mark.django_db
class TestScraperConfig:

  def test_constraint__unique_url(
      self,
      scraper_config: ScraperConfig,
  ) -> None:
    scraper_config2 = ScraperConfig(
        scraper=scraper_config.scraper,
        url=scraper_config.url,
    )

    with pytest.raises(ValidationError) as exc:
      scraper_config2.save()

    assert str(exc.value) == str(
        {
            "__all__": ["Constraint “URL name must be unique” is violated."],
        }
    )

  def test_has_item__no_related_item__returns_false(
      self,
      scraper_config: ScraperConfig,
  ) -> None:
    assert scraper_config.has_item is False

  def test_has_item__with_related_item__returns_true(
      self,
      item_scraper_config: ItemScraperConfig,
  ) -> None:
    assert item_scraper_config.scraper_config.has_item is True

  def test_associated_item__no_related_item__returns_none(
      self,
      scraper_config: ScraperConfig,
  ) -> None:
    assert scraper_config.associated_item is None

  def test_associated_item__with_related_item__returns_item(
      self,
      item_scraper_config: ItemScraperConfig,
  ) -> None:
    assert item_scraper_config.scraper_config.associated_item == (
        item_scraper_config.item
    )

  def test_clean__matching_scraper_regex__no_exception(
      self,
      scraper: Scraper,
  ) -> None:
    scraper.url_validation_regex = "^(http://)*(.*)"
    scraper.save()

    scraper_config = ScraperConfig(
        scraper=scraper,
        url="http://yahoo.com",
    )
    scraper_config.save()

  def test_clean__matching_scraper_regex__saves_url_as_regex_capture_group(
      self,
      scraper: Scraper,
  ) -> None:
    scraper.url_validation_regex = "^(http://)*(.*)"
    scraper.save()

    scraper_config = ScraperConfig(
        scraper=scraper,
        url="http://yahoo.com",
    )
    scraper_config.save()

  def test_clean__non_matching_scraper_regex__raises_exception(
      self,
      scraper: Scraper,
  ) -> None:
    scraper.url_validation_regex = "^(https://)(.*\\.ca)"
    scraper.save()

    with pytest.raises(ValidationError) as exc:
      scraper_config = ScraperConfig(
          scraper=scraper,
          url="http://yahoo.com",
      )
      scraper_config.save()

    assert str(exc.value) == str(
        {"url": [f"Invalid url for the {scraper.name} scraper."]}
    )

  def test_str__returns_scraper_name(
      self,
      scraper_config: ScraperConfig,
  ) -> None:
    assert str(
        scraper_config
    ) == f"{scraper_config.scraper.name}: {scraper_config.url}"
