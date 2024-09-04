"""Test the ScraperSerializer class."""

import pytest
from rest_framework.exceptions import ErrorDetail, ValidationError
from scrapers.models import Scraper
from scrapers.models.scraper import CONSTRAINT_NAMES
from scrapers.models.serializers.scraper import ScraperSerializer


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
        'pricing_selector': scraper.pricing_selector,
        'pricing_regex': scraper.pricing_regex,
        'pricing_bulk_selector': scraper.pricing_bulk_selector,
        'pricing_bulk_regex': scraper.pricing_bulk_regex,
        'url_validation_regex': scraper.url_validation_regex,
    }

  def test_deserialization__valid_input__correct_model(self) -> None:
    scraper_data = {
        'name': "mocked scraper.name",
        'pricing_selector': "mocked scraper.pricing_selector",
        'pricing_regex': "mocked scraper.pricing_regex",
        'pricing_bulk_selector': "mocked scraper.pricing_bulk_selector",
        'pricing_bulk_regex': "mocked scraper.pricing_bulk_rege",
        'url_validation_regex': "mocked scraper.url_validation_regex",
    }

    serialized = ScraperSerializer(data=scraper_data)
    serialized.is_valid(raise_exception=True)
    serialized.save()

  def test_deserialization__invalid_input__exception(self) -> None:
    scraper_data = {
        'name': "mocked scraper.name",
        'pricing_selector': "mocked scraper.pricing_selector",
        'pricing_regex': "mocked scraper.pricing_regex",
        'pricing_bulk_selector': "mocked scraper.pricing_bulk_selector",
        'pricing_bulk_regex': "mocked scraper.pricing_bulk_rege",
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

  def test_deserialization__enforces_unique_name_constraint(
      self,
      scraper: Scraper,
  ) -> None:
    serialized = ScraperSerializer(scraper)
    data = dict(serialized.data)
    data.pop('id')

    serializer = ScraperSerializer(data=data)

    with pytest.raises(ValidationError) as exc:
      serializer.is_valid(raise_exception=True)

    assert str(exc.value) == str(
        {
            'name':
                [
                    ErrorDetail(
                        string=CONSTRAINT_NAMES['name'],
                        code='invalid',
                    ),
                ]
        }
    )
