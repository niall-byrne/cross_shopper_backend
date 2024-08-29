"""Test the validator_greater_than_zero function."""

from decimal import Decimal
from typing import Any

import pytest
from django.core.exceptions import ValidationError
from utilities.models.validators.greater_than_zero import (
    VALIDATION_ERROR,
    validator_greater_than_zero,
)


class TestValidatorGreaterThanZero:

  @pytest.mark.parametrize("value", [Decimal(0.01), 0.1, 1, 200])
  def test_greater_than_0__does_not_raise_exception(
      self,
      value: Any,
  ) -> None:
    validator_greater_than_zero(value)

  def test_is_0__raises_exception(self) -> None:
    with pytest.raises(ValidationError) as exc:
      validator_greater_than_zero(0)

    assert exc.value.args == (VALIDATION_ERROR, None, None)

  @pytest.mark.parametrize("value", [Decimal(-0.01), -0.1, -1, -200])
  def test_less_than_0__raises_exception(
      self,
      value: Any,
  ) -> None:
    with pytest.raises(ValidationError) as exc:
      validator_greater_than_zero(value)

    assert exc.value.args == (VALIDATION_ERROR, None, None)
