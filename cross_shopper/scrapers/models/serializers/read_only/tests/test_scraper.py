"""Test the ScraperSerializerRO class."""

import pytest
from rest_framework.exceptions import ErrorDetail, ValidationError
from scrapers.models import Scraper
from scrapers.models.scraper import CONSTRAINT_NAMES
from scrapers.models.serializers.read_only.scraper import ScraperSerializerRO


@pytest.mark.django_db
class TestScraperSerializerRO:

  def test_serialization__correct_representation(
      self,
      scraper: Scraper,
  ) -> None:
    serialized = ScraperSerializerRO(scraper)

    assert serialized.data == {
        "id": scraper.pk,
        "name": scraper.name,
        "url_validation_regex": scraper.url_validation_regex,
    }

  def test_deserialization__valid_input__correct_model(self) -> None:
    scraper_data = {
        "name":
            "mocked scraper.name",
        "url_validation_regex":
            "mocked scraper.url_validation_regex_with_(two)(capture_groups)",
    }

    serialized = ScraperSerializerRO(data=scraper_data)
    serialized.is_valid(raise_exception=True)
    serialized.save()

  def test_deserialization__invalid_input__exception(self) -> None:
    scraper_data = {
        "name": "mocked scraper.name",
    }

    with pytest.raises(ValidationError) as exc:
      serialized = ScraperSerializerRO(data=scraper_data)
      serialized.is_valid(raise_exception=True)

    assert str(exc.value) == str(
        {
            "url_validation_regex":
                [
                    ErrorDetail(
                        string="This field is required.",
                        code="required",
                    )
                ]
        }
    )

  def test_deserialization__enforces_unique_name_constraint(
      self,
      scraper: Scraper,
  ) -> None:
    serialized = ScraperSerializerRO(scraper)
    data = dict(serialized.data)
    data.pop("id")

    serializer = ScraperSerializerRO(data=data)

    with pytest.raises(ValidationError) as exc:
      serializer.is_valid(raise_exception=True)

    assert str(exc.value) == str(
        {
            "name":
                [
                    ErrorDetail(
                        string=CONSTRAINT_NAMES["name"],
                        code="invalid",
                    ),
                ]
        }
    )
