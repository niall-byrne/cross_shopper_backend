"""Test the ScraperConfigSerializer class."""

from typing import TYPE_CHECKING

import pytest
from rest_framework.exceptions import ErrorDetail, ValidationError
from scrapers.models.scraper_config import CONSTRAINT_NAMES, ScraperConfig
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
        "id": scraper_config.pk,
        "url": scraper_config.url,
        "scraper": scraper_config.scraper.name,
        "is_active": scraper_config.is_active,
    }

  def test_deserialization__valid_input__existing_scraper__correct_model(
      self,
      scraper: "Scraper",
  ) -> None:
    scraper_config_data = {
        "url": "https://somehost.com/additional/path1",
        "scraper": scraper.name,
    }

    serialized = ScraperConfigSerializer(data=scraper_config_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.url == "somehost.com/additional/path1"
    assert instance.scraper == scraper

  def test_deserialization__invalid_input__non_existing_scraper__exception(
      self,
  ) -> None:
    scraper_config_data = {
        "url": "https://somehost.com/additional/path2",
        "scraper": "non-existent",
    }

    with pytest.raises(ValidationError) as exc:
      serialized = ScraperConfigSerializer(data=scraper_config_data)
      serialized.is_valid(raise_exception=True)

    assert str(exc.value) == str(
        {
            "scraper":
                [
                    ErrorDetail(
                        string="Object with name=non-existent does not exist.",
                        code="does_not_exist"
                    ),
                ],
        }
    )

  def test_deserialization__enforces_unique_url_constraint(
      self,
      scraper_config: ScraperConfig,
  ) -> None:
    serialized = ScraperConfigSerializer(scraper_config)
    data = dict(serialized.data)
    data.pop("id")

    serializer = ScraperConfigSerializer(data=data)

    with pytest.raises(ValidationError) as exc:
      serializer.is_valid(raise_exception=True)

    assert str(exc.value) == str(
        {
            "url":
                [ErrorDetail(
                    string=CONSTRAINT_NAMES["url"],
                    code="invalid",
                ),]
        }
    )
