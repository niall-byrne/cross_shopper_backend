"""Test the BrandSerializer class."""

from typing import Dict

import pytest
from items.models import Brand
from rest_framework.exceptions import ErrorDetail, ValidationError
from ..brand import BrandSerializer


@pytest.mark.django_db
class TestBrandSerializer:

  def test_serialization__correct_representation(
      self,
      brand: Brand,
  ) -> None:
    serialized = BrandSerializer(brand)

    assert serialized.data == {
        'name': brand.name,
    }

  def test_deserialization__valid_input__correct_model(self) -> None:
    brand_data: Dict[str, str] = {
        'name': 'mock_brand_name',
    }

    serialized = BrandSerializer(data=brand_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.name == brand_data['name']

  def test_deserialization__invalid_input__exception(self) -> None:
    brand_data: Dict[str, str] = {}

    with pytest.raises(ValidationError) as exc:
      serialized = BrandSerializer(data=brand_data)
      serialized.is_valid(raise_exception=True)

    assert str(exc.value) == str(
        {
            'name':
                [
                    ErrorDetail(
                        string='This field is required.', code='required'
                    )
                ]
        }
    )
