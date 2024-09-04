"""Test the StoreSerializer class."""

from typing import TYPE_CHECKING

import pytest
from rest_framework.exceptions import ErrorDetail, ValidationError
from stores.models.serializers.franchise import FranchiseSerializer
from stores.models.serializers.store import StoreSerializer

if TYPE_CHECKING:  # no cover
  from scrapers.models import Scraper
  from stores.models import Franchise, Store


@pytest.mark.django_db
class TestStoreSerializer:

  def test_serialization__correct_representation(
      self,
      store: "Store",
  ) -> None:
    serialized = StoreSerializer(store)

    assert serialized.data == {
        "id": store.pk,
        "address":
            {
                "street_number": str(store.address.street_number),
                "street_name": store.address.route,
                "city": store.address.locality.name,
                "state": store.address.locality.state.name,
                "postal_code": store.address.locality.postal_code,
                "country": store.address.locality.state.country.name,
            },
        "franchise": FranchiseSerializer(store.franchise).data,
        "franchise_location": store.franchise_location,
    }

  def test_deserialization__valid_input__existing_franchise__correct_model(
      self,
      franchise: "Franchise",
  ) -> None:
    franchise_data = {
        "address":
            {
                "street_number": "1",
                "street_name": "mocked street",
                "city": "mocked locality",
                "state": "mocked state",
                "postal_code": "mocked postal code",
                "country": "mocked country",
            },
        "franchise": FranchiseSerializer(franchise).data,
        "franchise_location": "franchise location string",
    }

    serialized = StoreSerializer(data=franchise_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.franchise == franchise
    assert instance.franchise_location == franchise_data["franchise_location"]

  def test_deserialization__valid_input__constraint_violation__exception(
      self,
      store: "Store",
  ) -> None:
    store_data = StoreSerializer(store).data
    store_data["address"]["city"] = "some other city"

    with pytest.raises(ValidationError) as exc:
      serialized = StoreSerializer(data=store_data)
      serialized.is_valid(raise_exception=True)
      serialized.save()

    assert str(exc.value) == str(
        {
            "non_field_errors":
                [
                    ErrorDetail(
                        string=(
                            "The fields franchise, franchise_location "
                            "must make a unique set."
                        ),
                        code="unique",
                    )
                ]
        }
    )

  def test_deserialization__invalid_input__non_existing_franchise__exception(
      self, scraper: "Scraper"
  ) -> None:
    franchise_data = {
        "address":
            {
                "street_number": "1",
                "street_name": "mocked street",
                "city": "mocked locality",
                "state": "mocked state",
                "postal_code": "mocked postal code",
                "country": "mocked country",
            },
        "franchise":
            {
                "name": "non existing franchise",
                "scraper": scraper.name,
            },
        "franchise_location": "franchise location string",
    }

    with pytest.raises(ValidationError) as exc:
      serialized = StoreSerializer(data=franchise_data)
      serialized.is_valid(raise_exception=True)
      serialized.save()

    assert str(exc.value) == str(
        {
            "franchise":
                [
                    ErrorDetail(
                        string="Franchise matching query does not exist.",
                        code="does_not_exist",
                    )
                ]
        }
    )
