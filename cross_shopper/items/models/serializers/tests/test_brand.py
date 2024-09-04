"""Test the BrandSerializer class."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from items.models.serializers.brand import BrandSerializer
from rest_framework.exceptions import ErrorDetail, ValidationError

if TYPE_CHECKING:
  from items.models import Brand


@pytest.mark.django_db
class TestBrandSerializer:

  def test_serialization__correct_representation(
      self,
      brand: Brand,
  ) -> None:
    serialized = BrandSerializer(brand)

    assert serialized.data == {
        "name": brand.name,
    }

  def test_deserialization__valid_input__correct_model(self) -> None:
    brand_data: dict[str, str] = {
        "name": "mock_brand_name",
    }

    serialized = BrandSerializer(data=brand_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.name == brand_data["name"]

  def test_deserialization__invalid_input__exception(self) -> None:
    brand_data: dict[str, str] = {}

    with pytest.raises(ValidationError) as exc:
      serialized = BrandSerializer(data=brand_data)
      serialized.is_valid(raise_exception=True)

    assert str(exc.value) == str(
        {
            "name":
                [
                    ErrorDetail(
                        string="This field is required.", code="required"
                    )
                ]
        }
    )
