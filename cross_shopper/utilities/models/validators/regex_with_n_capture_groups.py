"""Regular Expression Validator."""

import re
from functools import lru_cache
from typing import Callable

from django.core.exceptions import ValidationError

VALIDATION_ERROR_PREFIX = "Regex: "
VALIDATION_ERROR_CAPTURE_GROUP_COUNT = "must contain exactly %s capture group(s)."


@lru_cache(maxsize=None)
def create_validator_regex_with_n_capture_groups(
    n: int,
) -> Callable[[str], None]:
  """Create a validator for a regex with a count of n capture groups."""

  def validator(value: str) -> None:
    """Validate a value is a compilable regex with n capture groups."""
    try:
      pattern = re.compile(value)
    except re.error as exc:
      raise ValidationError(VALIDATION_ERROR_PREFIX + exc.args[0])

    if pattern.groups != n:
      raise ValidationError(
          VALIDATION_ERROR_PREFIX + VALIDATION_ERROR_CAPTURE_GROUP_COUNT % n
      )

  return validator
