"""Test the BrandSerializerRW class."""

from typing import Dict

import pytest
from items.models import Brand
from items.models.serializers.read_write.brand import BrandSerializerRW
from rest_framework.exceptions import ErrorDetail, ValidationError


@pytest.mark.django_db
class TestBrandSerializerRW:

  def test_serialization__correct_representation(
      self,
      brand: Brand,
  ) -> None:
    serialized = BrandSerializerRW(brand)

    assert serialized.data == {
        'name': brand.name,
    }

  def test_deserialization__valid_input__correct_model(self) -> None:
    brand_data: Dict[str, str] = {
        'name': 'mock_brand_name',
    }

    serialized = BrandSerializerRW(data=brand_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.name == brand_data['name']

  def test_deserialization__invalid_input__exception(self) -> None:
    brand_data: Dict[str, str] = {}

    with pytest.raises(ValidationError) as exc:
      serialized = BrandSerializerRW(data=brand_data)
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
