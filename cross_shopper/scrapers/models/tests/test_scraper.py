"""Test the Scraper model."""

import pytest
from django.core.exceptions import ValidationError
from scrapers.models.scraper import CONSTRAINT_NAMES, Scraper


@pytest.mark.django_db
class TestScraper:

  def test_name__is_unique(self) -> None:
    scraper_data = {
        "name":
            "mocked name",
        "url_validation_regex":
            "mocked_url_validation_regex_with_(two)(capture_groups)",
    }

    scraper1 = Scraper(**scraper_data)
    scraper1.save()

    with pytest.raises(ValidationError) as exc:
      scraper2 = Scraper(**scraper_data)
      scraper2.save()

    assert str(exc.value) == str(
        {
            '__all__':
                [
                    'Constraint '
                    f'“{CONSTRAINT_NAMES["name"]}” '
                    'is violated.',
                ]
        }
    )

  def test_url_validation_regex__must_contain_2_capture_groups(self) -> None:
    scraper_data = {
        "name":
            "mocked name",
        "url_validation_regex":
            "mocked_url_validation_regex_with_no_capture_groups",
    }

    with pytest.raises(ValidationError) as exc:
      scraper1 = Scraper(**scraper_data)
      scraper1.save()

    assert str(exc.value) == str(
        {
            'url_validation_regex':
                ['Regex: must contain exactly 2 capture group(s).']
        }
    )

  def test_str__returns_scraper_name(self, scraper: Scraper) -> None:
    assert str(scraper) == scraper.name
