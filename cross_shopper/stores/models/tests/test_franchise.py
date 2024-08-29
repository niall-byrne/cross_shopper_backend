"""Test the Franchise model."""

from typing import TYPE_CHECKING

import pytest
from django.core.exceptions import ValidationError
from stores.models.franchise import CONSTRAINT_NAMES, Franchise

if TYPE_CHECKING:  # no cover
  from scrapers.models import Scraper


@pytest.mark.django_db
class TestFranchise:

  def test_name(self, scraper: "Scraper") -> None:
    franchise_data = {"name": "mocked name", "scraper": scraper}

    franchise1 = Franchise(**franchise_data)
    franchise1.save()

    with pytest.raises(ValidationError) as exc:
      franchise2 = Franchise(**franchise_data)
      franchise2.save()

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

  def test_str__returns_franchise_name(self, franchise: Franchise) -> None:
    assert str(franchise) == franchise.name
