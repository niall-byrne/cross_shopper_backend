"""Regular Expression Validator."""

import re

from django.core.exceptions import ValidationError

VALIDATION_ERROR_PREFIX = "Regex: "


def validator_regex(value: str) -> None:
  """Validate a value is a compilable regex."""
  try:
    re.compile(value)
  except re.error as exc:
    raise ValidationError(VALIDATION_ERROR_PREFIX + exc.args[0],)
