"""Test the ScraperConfigSerializer class."""

from typing import TYPE_CHECKING

import pytest
from scrapers.models import ScraperConfig
from scrapers.models.serializers.scraper_config import ScraperConfigSerializer

if TYPE_CHECKING:  # no cover
  from scrapers.models import Scraper


@pytest.mark.django_db
class TestScraperConfigSerializer:

  def test_serialization__correct_representation(
      self,
      scraper_config: ScraperConfig,
  ) -> None:
    serialized = ScraperConfigSerializer(scraper_config)

    assert serialized.data == {
        'url': scraper_config.url,
        'scraper': scraper_config.scraper.name,
    }

  def test_deserialization__valid_input__existing_scraper__correct_model(
      self,
      scraper: "Scraper",
  ) -> None:
    scraper_config_data = {
        'url': scraper.url_validation_regex + '/additional/path',
        'scraper': scraper.name,
    }

    serialized = ScraperConfigSerializer(data=scraper_config_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.url == scraper_config_data['url']
    assert instance.scraper == scraper

  def test_deserialization__invalid_input__non_existing_scraper__exception(
      self,
      scraper: "Scraper",
  ) -> None:
    scraper_config_data = {
        'url': scraper.url_validation_regex + '/additional/path',
        'scraper': scraper.name,
    }

    serialized = ScraperConfigSerializer(data=scraper_config_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.url == scraper_config_data['url']
    assert instance.scraper == scraper
