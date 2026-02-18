"""Test the ScraperSerializer class."""

import pytest
from rest_framework.exceptions import ErrorDetail, ValidationError
from scrapers.models import Scraper
from ..scraper import ScraperSerializer


@pytest.mark.django_db
class TestScraperSerializer:

  def test_serialization__correct_representation(
      self,
      scraper: Scraper,
  ) -> None:
    serialized = ScraperSerializer(scraper)

    assert serialized.data == {
        'id': scraper.id,
        'name': scraper.name,
        'url_validation_regex': scraper.url_validation_regex,
    }

  def test_deserialization__valid_input__correct_model(self) -> None:
    scraper_data = {
        'name':
            "mocked scraper.name",
        'url_validation_regex':
            "mocked scraper.url_validation_regex_with_(two)(capture_groups)",
    }

    serialized = ScraperSerializer(data=scraper_data)
    serialized.is_valid(raise_exception=True)
    serialized.save()

  def test_deserialization__invalid_input__exception(self) -> None:
    scraper_data = {
        'name': "mocked scraper.name",
    }

    with pytest.raises(ValidationError) as exc:
      serialized = ScraperSerializer(data=scraper_data)
      serialized.is_valid(raise_exception=True)

    assert str(exc.value) == str(
        {
            'url_validation_regex':
                [
                    ErrorDetail(
                        string='This field is required.',
                        code='required',
                    )
                ]
        }
    )
