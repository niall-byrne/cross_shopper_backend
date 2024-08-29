"""Greater Than Zero Value Validator."""

from typing import Any

from django.core.exceptions import ValidationError

VALIDATION_ERROR = 'This value must be greater than zero.'


def validator_greater_than_zero(value: Any) -> None:
  """Validate a value is greater than zero."""
  if value <= 0:
    raise ValidationError(VALIDATION_ERROR)
