"""Test the create_restricted_values_validator function."""
from __future__ import annotations

from typing import Any

import pytest
from django.core.exceptions import ValidationError
from utilities.models.validators.restricted_values import (
    VALIDATION_ERROR,
    create_restricted_values_validator,
)


class TestValidatorRestrictedValues:

  @pytest.mark.parametrize(
      "restricted_values", [
          frozenset({1}),
          frozenset({2, 3}),
          frozenset({1, 2, 3}),
      ]
  )
  def test_generated_validator__is_cached(
      self,
      restricted_values: frozenset[Any],
  ) -> None:
    validator1 = create_restricted_values_validator(restricted_values)
    validator2 = create_restricted_values_validator(restricted_values)

    assert validator1 == validator2

  @pytest.mark.parametrize(
      "value,restricted_values", [
          (
              None,
              frozenset({1}),
          ),
          (
              "Hello",
              frozenset({2, None}),
          ),
          (
              123,
              frozenset({"A", "B", None}),
          ),
      ]
  )
  def test_generated_validator__not_coerced__not_restricted__no_exception(
      self,
      value: Any,
      restricted_values: frozenset[Any],
  ) -> None:
    validator = create_restricted_values_validator(restricted_values)

    validator(value)

  @pytest.mark.parametrize(
      "value,restricted_values", [
          (
              123,
              frozenset({"A", "B", None}),
          ),
      ]
  )
  def test_generated_validator__coerced__not_restricted__no_exception(
      self,
      value: Any,
      restricted_values: frozenset[Any],
  ) -> None:
    validator = create_restricted_values_validator(
        restricted_values,
        coerce_to_str=True,
    )

    validator(value)

  @pytest.mark.parametrize(
      "value,restricted_values,invalid_value", [
          (
              None,
              frozenset({None}),
              None,
          ),
          (
              "Hello",
              frozenset({2, None, "H"}),
              "H",
          ),
          (
              123,
              frozenset({"A", 123, None}),
              123,
          ),
      ]
  )
  def test_generated_validator__not_coerced__restricted_value__raises_exception(
      self,
      value: Any,
      restricted_values: frozenset[Any],
      invalid_value: Any,
  ) -> None:
    validator = create_restricted_values_validator(restricted_values)

    with pytest.raises(ValidationError) as exc:
      validator(value)

    assert str(exc.value.args[0]) == VALIDATION_ERROR % str(invalid_value)

  @pytest.mark.parametrize(
      "value,restricted_values,invalid_value", [
          (
              None,
              frozenset({None}),
              None,
          ),
          (
              "Hello",
              frozenset({2, None, "H"}),
              "H",
          ),
          (
              123,
              frozenset({"A", 2, None}),
              2,
          ),
      ]
  )
  def test_generated_validator__coerced__restricted_value__raises_exception(
      self,
      value: Any,
      restricted_values: frozenset[Any],
      invalid_value: Any,
  ) -> None:
    validator = create_restricted_values_validator(
        restricted_values,
        coerce_to_str=True,
    )

    with pytest.raises(ValidationError) as exc:
      validator(value)

    assert str(exc.value.args[0]) == VALIDATION_ERROR % str(invalid_value)
