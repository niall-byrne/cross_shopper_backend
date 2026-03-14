"""Test the MultiFieldValidator class."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # no cover
  from typing import Any, Mapping
  from unittest.mock import MagicMock

  from .conftest import ConcreteMultiFieldValidator


class TestMultiFieldValidator:

  def test_generate_model_error__returns_django_validation_error(
      self,
      concrete_validator: "ConcreteMultiFieldValidator",
  ) -> None:
    from django.core.exceptions import ValidationError as DjangoValidationError

    expected_message = "Error for ['field1', 'field2'] with extra"

    result = concrete_validator.generate_model_error()

    assert isinstance(result, DjangoValidationError)
    assert result.message_dict == {
        "field1": [expected_message],
        "field2": [expected_message],
    }

  def test_generate_serializer_error__returns_serializer_validation_error(
      self,
      concrete_validator: "ConcreteMultiFieldValidator",
  ) -> None:
    from rest_framework.exceptions import (
        ValidationError as SerializerValidationError,
    )

    expected_message = "Error for ['field1', 'field2'] with extra"

    result = concrete_validator.generate_serializer_error()

    assert isinstance(result, SerializerValidationError)
    assert result.detail == {
        "field1": [expected_message],
        "field2": [expected_message],
    }

  def test_get_attr__fully_serialized_model__returns_value(
      self,
      concrete_validator: "ConcreteMultiFieldValidator",
      mocked_serialized_model_full: "Mapping[str, Any]",
  ) -> None:
    result = concrete_validator.get_attr(
        mocked_serialized_model_full,
        "nested.field2",
    )

    assert result == "value2"

  def test_get_attr__partially_serialized_model__returns_value(
      self,
      concrete_validator: "ConcreteMultiFieldValidator",
      mocked_serialized_model_partial: "Mapping[str, Any]",
  ) -> None:
    result = concrete_validator.get_attr(
        mocked_serialized_model_partial,
        "nested.model.field1",
    )

    assert result == "value1"

  def test_attr__unserialized_model__returns_value(
      self,
      concrete_validator: "ConcreteMultiFieldValidator",
      mocked_model: "MagicMock",
  ) -> None:
    result = concrete_validator.get_attr(
        mocked_model,
        "nested.field2",
    )

    assert result == "value2"
