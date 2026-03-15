"""Test the MultiFieldValidator class."""

from typing import Any, Mapping
from unittest.mock import MagicMock

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import (
    ValidationError as SerializerValidationError,
)
from cross_shopper.utilities.models.validators.tests.multi_field_validator.helpers import (
    ConcreteMultiFieldValidator,
)


class TestMultiFieldValidator:

  def test_generate_model_error__interpolates_message__returns_django_validation_error(
      self,
      concrete_validator: ConcreteMultiFieldValidator,
  ) -> None:
    expected_message = "Error for ['field1', 'field2'] with extra"

    result = concrete_validator.generate_model_error()

    assert isinstance(result, DjangoValidationError)
    assert result.message_dict == {
        "field1": [expected_message],
        "field2": [expected_message],
    }

  def test_generate_serializer_error__interpolates_message__returns_serializer_validation_error(
      self,
      concrete_validator: ConcreteMultiFieldValidator,
  ) -> None:
    expected_message = "Error for ['field1', 'field2'] with extra"

    result = concrete_validator.generate_serializer_error()

    assert isinstance(result, SerializerValidationError)
    assert result.detail == {
        "field1": [expected_message],
        "field2": [expected_message],
    }

  def test_model_get__valid_path__returns_value(
      self,
      concrete_validator: ConcreteMultiFieldValidator,
      mocked_model: MagicMock,
  ) -> None:
    result = concrete_validator.model_get("nested.field2", mocked_model)

    assert result == "value2"

  def test_deserialized_model_get__valid_path__returns_value(
      self,
      concrete_validator: ConcreteMultiFieldValidator,
      mocked_serializer_data: Mapping[str, Any],
  ) -> None:
    result = concrete_validator.deserialized_model_get(
        "nested.field2", mocked_serializer_data)

    assert result == "value2"

  def test_deserialized_model_get__model_instance_in_path__returns_value(
      self,
      concrete_validator: ConcreteMultiFieldValidator,
      mocked_model: MagicMock,
  ) -> None:
    data = {"model": mocked_model}

    result = concrete_validator.deserialized_model_get("model.field1", data)

    assert result == "value1"
