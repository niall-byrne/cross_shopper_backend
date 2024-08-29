"""Test the Scraper model."""

import pytest
from django.core.exceptions import ValidationError
from scrapers.models.scraper import CONSTRAINT_NAMES, Scraper


@pytest.mark.django_db
class TestScraper:

  def test_name__is_unique(self) -> None:
    scraper_data = {
        "name": "mocked name",
        "pricing_selector": "mocked_pricing_selector",
        "pricing_regex": "mocked_pricing_regex",
        "pricing_bulk_selector": "mocked_pricing_bulk_selector",
        "pricing_bulk_regex": "mocked_pricing_bulk_regex",
        "url_validation_regex": "mocked_url_validation_regex",
    }

    scraper1 = Scraper(**scraper_data)
    scraper1.save()

    with pytest.raises(ValidationError) as exc:
      scraper2 = Scraper(**scraper_data)
      scraper2.save()

    assert str(exc.value) == str(
        {"__all__": [f"Constraint “{CONSTRAINT_NAMES['name']}” is violated.",]}
    )

  def test_str__returns_scraper_name(self, scraper: Scraper) -> None:
    assert str(scraper) == scraper.name
