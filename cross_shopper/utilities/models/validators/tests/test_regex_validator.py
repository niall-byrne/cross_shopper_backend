"""Test the validator_regex function."""

import pytest
from django.core.exceptions import ValidationError
from utilities.models.validators.regex import (
    VALIDATION_ERROR_PREFIX,
    validator_regex,
)


class TestValidatorRegex:

  @pytest.mark.parametrize(
      "value", ["string", "capture (group)", ".*wildcard.*"]
  )
  def test_compilable_regex__does_not_raise_exception(
      self,
      value: str,
  ) -> None:
    validator_regex(value)

  @pytest.mark.parametrize(
      "value",
      [
          "unbalanced capture group)",
          "*invalid wildcard",
          "[invalid character range",
      ],
  )
  def test_uncompilable_regex__raises_exception(
      self,
      value: str,
  ) -> None:
    with pytest.raises(ValidationError) as exc:
      validator_regex(value)

    assert str(exc.value.args[0]).startswith(VALIDATION_ERROR_PREFIX)
