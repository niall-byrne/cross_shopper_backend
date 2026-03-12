"""Test the PriceGroupSerializerRW class."""

from typing import TYPE_CHECKING

import pytest
from items.models import PackagingUnit, PriceGroup
from items.models.serializers.read_write.price_group import (
    PriceGroupSerializerRW,
)
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail, ValidationError

if TYPE_CHECKING:  # no cover
  from typing import Dict, Union


@pytest.mark.django_db
class TestPriceGroupSerializerRW:

  def test_serialization__correct_representation(
      self,
      price_group: PriceGroup,
  ) -> None:
    serialized = PriceGroupSerializerRW(price_group)

    assert serialized.data == {
        'name': price_group.name,
        'quantity': price_group.quantity,
        'unit': price_group.unit.name,
    }

  def test_deserialization__valid_input__existing_group__correct_model(
      self,
      price_group: PriceGroup,
  ) -> None:
    price_group_data: "Dict[str, Union[int, str]]" = {
        'name': price_group.name,
    }

    serialized = PriceGroupSerializerRW(data=price_group_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.name == price_group.name
    assert instance.quantity == price_group.quantity
    assert instance.unit.name == price_group.unit.name

  def test_deserialization__valid_input__no_existing_components__correct_model(
      self,
  ) -> None:
    price_group_data: "Dict[str, Union[int, str]]" = {
        'name': 'MOCKED PRICE GROUP NAME',
        'quantity': 3,
        'unit': 'MOCKED PRICE GROUP UNIT',
    }

    serialized = PriceGroupSerializerRW(data=price_group_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.name == price_group_data['name']
    assert instance.quantity == price_group_data['quantity']
    assert instance.unit.name == price_group_data['unit']

  def test_deserialization__valid_input__existing_components__correct_model(
      self,
      packaging_unit: PackagingUnit,
  ) -> None:
    price_group_data: "Dict[str, Union[int, str]]" = {
        'name': 'MOCKED PRICE GROUP NAME',
        'quantity': 3,
        'unit': packaging_unit.name,
    }

    serialized = PriceGroupSerializerRW(data=price_group_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.name == price_group_data['name']
    assert instance.quantity == price_group_data['quantity']
    assert instance.unit.name == price_group_data['unit']

  @pytest.mark.parametrize("missing_field", ("name", "quantity", "unit"))
  def test_deserialization__invalid_input__no_existing_components__exception(
      self,
      missing_field: str,
  ) -> None:
    price_group_data: "Dict[str, Union[int, str]]" = {
        'name': 'MOCKED PRICE GROUP NAME',
        'quantity': 3,
        'unit': 'MOCKED PRICE GROUP UNIT',
    }
    del price_group_data[missing_field]

    serialized = PriceGroupSerializerRW(data=price_group_data)

    with pytest.raises(ValidationError) as exc:
      serialized.is_valid(raise_exception=True)

    assert str(exc.value) == str(
        {
            missing_field:
                [
                    ErrorDetail(
                        string=str(
                            serializers.Field.default_error_messages['required']
                        ),
                        code='required'
                    )
                ]
        }
    )
