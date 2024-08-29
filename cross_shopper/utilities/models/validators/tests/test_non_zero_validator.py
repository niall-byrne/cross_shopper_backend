"""Test the validator_non_zero function."""

from typing import Any

import pytest
from django.core.exceptions import ValidationError
from utilities.models.validators.non_zero import (
    VALIDATION_ERROR,
    validator_non_zero,
)


class TestValidatorNonZero:

  @pytest.mark.parametrize("value", [1, "A", None, 200])
  def test_non_zero_value__does_not_raise_exception(
      self,
      value: Any,
  ) -> None:
    validator_non_zero(value)

  def test_is_zero__raises_exception(self,) -> None:
    with pytest.raises(ValidationError) as exc:
      validator_non_zero(0)

    assert exc.value.args == (VALIDATION_ERROR, None, None)
