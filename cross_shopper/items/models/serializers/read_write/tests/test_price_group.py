"""Test the PriceGroupSerializerRW class."""

from typing import TYPE_CHECKING

import pytest
from items.models import PriceGroup
from items.models.serializers.read_write.price_group import (
    PriceGroupSerializerRW,
)
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail, ValidationError

if TYPE_CHECKING:  # no cover
  from typing import Dict, List, Union

  from items.models import Attribute, Item, PackagingUnit
  AliasPriceGroupData = Dict[str, Union[int, str, bool, List[str]]]


@pytest.mark.django_db
class TestPriceGroupSerializerRW:

  def test_serialization__correct_representation(
      self,
      price_group: PriceGroup,
  ) -> None:
    serialized = PriceGroupSerializerRW(price_group)

    assert serialized.data == {
        'id': price_group.pk,
        'is_non_gmo': price_group.is_non_gmo,
        'is_organic': price_group.is_organic,
        'name': price_group.name,
        'quantity': price_group.quantity,
        'unit': price_group.unit.name,
    }

  def test_deserialization__valid_input__new__correct_model(self,) -> None:
    price_group_data: "AliasPriceGroupData" = {
        'attribute': [
            "new_attribute1",
            "new_attribute2",
        ],
        'is_non_gmo': False,
        'is_organic': False,
        'name': "mock price group name",
        'quantity': 1,
        'unit': "mock unit",
    }

    serialized = PriceGroupSerializerRW(data=price_group_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert [attr.name for attr in instance.attribute.all()] == \
      price_group_data['attribute']
    assert instance.is_non_gmo == price_group_data['is_non_gmo']
    assert instance.is_organic == price_group_data['is_organic']
    assert instance.name == price_group_data['name']
    assert instance.quantity == price_group_data['quantity']
    assert instance.unit.name == price_group_data['unit']

  def test_deserialization__valid_input__new__default_attributes__correct_model(
      self,
  ) -> None:
    price_group_data: "AliasPriceGroupData" = {
        'is_non_gmo': False,
        'is_organic': False,
        'name': "mock price group name",
        'quantity': 1,
        'unit': "mock unit",
    }

    serialized = PriceGroupSerializerRW(data=price_group_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.attribute.count() == 0
    assert instance.is_non_gmo == price_group_data['is_non_gmo']
    assert instance.is_organic == price_group_data['is_organic']
    assert instance.name == price_group_data['name']
    assert instance.quantity == price_group_data['quantity']
    assert instance.unit.name == price_group_data['unit']

  def test_deserialization__valid_input__existing__correct_model(
      self,
      attribute: "Attribute",
      packaging_unit: "PackagingUnit",
  ) -> None:
    price_group_data: "AliasPriceGroupData" = {
        'attribute': [attribute.name],
        'is_non_gmo': True,
        'is_organic': False,
        'name': "mock name",
        'quantity': 100,
        'unit': packaging_unit.name,
    }

    serialized = PriceGroupSerializerRW(data=price_group_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert [attr.pk for attr in instance.attribute.all()] == [attribute.pk]
    assert instance.is_non_gmo == price_group_data['is_non_gmo']
    assert instance.is_organic == price_group_data['is_organic']
    assert instance.name == price_group_data['name']
    assert instance.quantity == price_group_data['quantity']
    assert instance.unit.pk == packaging_unit.pk

  @pytest.mark.parametrize("missing_field", ("name", "quantity"))
  def test_deserialization__invalid_input__missing_field__exception(
      self,
      item: "Item",
      missing_field: str,
  ) -> None:
    price_group_data: "AliasPriceGroupData" = {
        'attribute': [
            "new_attribute1",
            "new_attribute2",
        ],
        'is_non_gmo': item.price_group.is_non_gmo,
        'is_organic': item.price_group.is_organic,
        'name': item.price_group.name,
        'quantity': item.price_group.quantity,
        'unit': item.price_group.unit.name,
    }
    del price_group_data[missing_field]

    serialized = PriceGroupSerializerRW(
        data=price_group_data,
        context={"item": item},
    )

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
