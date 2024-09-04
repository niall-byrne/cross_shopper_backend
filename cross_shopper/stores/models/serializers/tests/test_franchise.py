"""Test the FranchiseSerializer class."""

from typing import TYPE_CHECKING

import pytest
from rest_framework.exceptions import ErrorDetail, ValidationError
from stores.models.serializers.franchise import FranchiseSerializer

if TYPE_CHECKING:  # no cover
  from scrapers.models import Scraper
  from stores.models.franchise import Franchise


@pytest.mark.django_db
class TestFranchiseSerializer:

  def test_serialization__correct_representation(
      self,
      franchise: "Franchise",
  ) -> None:
    serialized = FranchiseSerializer(franchise)

    assert serialized.data == {
        "name": franchise.name,
        "scraper": str(franchise.scraper),
    }

  def test_deserialization__valid_input__existing_scraper__correct_model(
      self,
      scraper: "Scraper",
  ) -> None:
    franchise_data = {
        "name": "mock_franchise_name",
        "scraper": scraper.name,
    }

    serialized = FranchiseSerializer(data=franchise_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.name == franchise_data["name"]
    assert instance.scraper == scraper

  def test_deserialization__invalid_input__non_existing_scraper__exception(
      self,
      scraper: "Scraper",
  ) -> None:
    franchise_data = {
        "name": "mock_franchise_name",
        "scraper": "non existing scraper",
    }

    with pytest.raises(ValidationError) as exc:
      serialized = FranchiseSerializer(data=franchise_data)
      serialized.is_valid(raise_exception=True)

    assert str(exc.value) == str(
        {
            "scraper":
                [
                    ErrorDetail(
                        string=(
                            "Object with name=non existing scraper "
                            "does not exist."
                        ),
                        code="does_not_exist",
                    )
                ]
        }
    )
