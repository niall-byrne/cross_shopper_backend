"""Test the PackagingSerializer class."""

from typing import Any, Dict, Optional, Union

import pytest
from items.models import Packaging
from rest_framework.exceptions import ErrorDetail, ValidationError
from ..packaging import PackagingSerializer


@pytest.mark.django_db
class TestPackagingSerializer:

  def test_serialization__bulk__correct_representation(
      self,
      packaging_as_bulk: Packaging,
  ) -> None:
    serialized = PackagingSerializer(packaging_as_bulk)

    assert serialized.data == {
        'quantity': packaging_as_bulk.quantity,
        'unit': packaging_as_bulk.unit.name,
        'container': packaging_as_bulk.container,
    }

  def test_serialization__non_bulk__correct_representation(
      self,
      packaging_as_non_bulk: Packaging,
  ) -> None:
    assert packaging_as_non_bulk.unit is not None
    assert packaging_as_non_bulk.container is not None
    serialized = PackagingSerializer(packaging_as_non_bulk)

    assert serialized.data == {
        'quantity': str(packaging_as_non_bulk.quantity),
        'unit': packaging_as_non_bulk.unit.name,
        'container': packaging_as_non_bulk.container.name,
    }

  def test_deserialization__valid_input__no_existing_components__correct_model(
      self,
  ) -> None:
    packaging_data: Dict[str, Union[int, str]] = {
        'quantity': 3,
        'unit': 'MOCKED PACKAGING UNIT',
        'container': 'mocked packaging container',
    }

    serialized = PackagingSerializer(data=packaging_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.quantity == packaging_data['quantity']
    assert isinstance(packaging_data['unit'], str)
    assert instance.unit.name == packaging_data['unit']
    assert isinstance(packaging_data['container'], str)
    assert instance.container.name == packaging_data['container'].capitalize()

  def test_deserialization__valid_input__existing_components__correct_model(
      self,
      packaging_as_non_bulk: Packaging,
  ) -> None:
    assert packaging_as_non_bulk.container is not None
    packaging_data: Dict[str, Any] = {
        'quantity': 3,
        'unit': 'MOCKED PACKAGING UNIT',
        'container': packaging_as_non_bulk.container.name,
    }

    serialized = PackagingSerializer(data=packaging_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.quantity == packaging_data['quantity']
    assert isinstance(packaging_data['unit'], str)
    assert instance.unit.name == packaging_data['unit']
    assert instance.container == packaging_as_non_bulk.container

  @pytest.mark.parametrize(
      "field_name,error_message,error_code", [
          (
              "quantity", PackagingSerializer.ERROR_MESSAGE_QUANTITY_IS_NULL,
              "invalid"
          ),
          ("unit", "This field may not be null.", "null"),
          (
              "container", PackagingSerializer.ERROR_MESSAGE_CONTAINER_IS_NULL,
              "invalid"
          ),
      ]
  )
  def test_deserialization__vary_invalid_input__raises_exception(
      self,
      packaging_as_non_bulk: Packaging,
      field_name: str,
      error_message: str,
      error_code: str,
  ) -> None:
    packaging_data: Dict[str, Optional[Union[int, str]]] = {
        'quantity': 3,
        'unit': 'MOCKED PACKAGING UNIT',
        'container': "mocked container",
    }

    packaging_data[field_name] = None

    with pytest.raises(ValidationError) as exc:
      serialized = PackagingSerializer(data=packaging_data)
      serialized.is_valid(raise_exception=True)

    assert str(exc.value) == str(
        {field_name: [ErrorDetail(string=error_message, code=error_code)]}
    )
