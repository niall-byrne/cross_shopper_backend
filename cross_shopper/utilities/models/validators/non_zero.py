"""Non-Zero Value Validator."""

from typing import Any

from django.core.exceptions import ValidationError

VALIDATION_ERROR = 'This value cannot be zero.'


def validator_non_zero(value: Any) -> None:
  """Validate a value is not equal to zero."""
  if value == 0:
    raise ValidationError(VALIDATION_ERROR)
