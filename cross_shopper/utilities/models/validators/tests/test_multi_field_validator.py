"""Test the MultiFieldValidator class."""

from unittest.mock import Mock

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import (
    ValidationError as RestFrameworkValidationError,
)
from utilities.models.validators.tests.__helper__ import (
    ConcreteMultiFieldValidator,
)


class TestMultiFieldValidator:

  def test_is_model_valid__instance_is_valid__returns_true(
      self,
      multi_field_validator: ConcreteMultiFieldValidator,
      mocked_model_instance: Mock,
  ) -> None:
    mocked_model_instance.is_valid = True

    result = multi_field_validator.is_model_valid(mocked_model_instance)

    assert result is True

  def test_is_model_valid__instance_is_invalid__returns_false(
      self,
      multi_field_validator: ConcreteMultiFieldValidator,
      mocked_model_instance: Mock,
  ) -> None:
    mocked_model_instance.is_valid = False

    result = multi_field_validator.is_model_valid(mocked_model_instance)

    assert result is False

  def test_generate_model_error__valid_input__returns_django_validation_error(
      self,
      multi_field_validator: ConcreteMultiFieldValidator,
  ) -> None:
    expected_message = "Error in ['field1', 'field2']"

    result = multi_field_validator.generate_model_error()

    assert isinstance(result, DjangoValidationError)
    assert result.message_dict == {
        "field1": [expected_message],
        "field2": [expected_message],
    }

  def test_generate_serializer_error__valid_input__returns_drf_validation_error(
      self,
      multi_field_validator: ConcreteMultiFieldValidator,
  ) -> None:
    expected_message = "Error in ['field1', 'field2']"

    result = multi_field_validator.generate_serializer_error()

    assert isinstance(result, RestFrameworkValidationError)
    assert result.detail == {
        "field1": [expected_message],
        "field2": [expected_message],
    }
