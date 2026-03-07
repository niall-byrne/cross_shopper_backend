"""Restricted Values Validator."""
from __future__ import annotations

from collections.abc import Iterable
from functools import lru_cache
from typing import Any, Callable

from django.core.exceptions import ValidationError

VALIDATION_ERROR = "The value '%s' is restricted."


@lru_cache(maxsize=None)
def create_restricted_values_validator(
    restricted_values: frozenset[Any],
    coerce_to_str: bool = False,
) -> Callable[[Any], None]:
  """Create a validator for restricted values."""

  def raise_error(restricted_value: Any) -> None:
    raise ValidationError(VALIDATION_ERROR % str(restricted_value))

  def validator(value: Any) -> None:
    """Validate a value does not contain any of a set of restricted values."""
    if coerce_to_str:
      value = str(value)

    is_iterable = isinstance(value, Iterable)

    for restricted_value in restricted_values:
      if coerce_to_str:
        restricted_value = str(restricted_value)

      if restricted_value == value:
        raise_error(restricted_value)

      if is_iterable:
        try:
          if restricted_value in value:
            raise_error(restricted_value)
        except TypeError:
          pass

  return validator
