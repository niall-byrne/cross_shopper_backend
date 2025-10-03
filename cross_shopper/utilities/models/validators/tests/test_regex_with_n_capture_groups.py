"""Test the validator_regex function."""

import pytest
from django.core.exceptions import ValidationError
from ..regex_with_n_capture_groups import (
    VALIDATION_ERROR_CAPTURE_GROUP_COUNT,
    VALIDATION_ERROR_PREFIX,
    create_validator_regex_with_n_capture_groups,
)


class TestValidatorRegexWithNCaptureGroups:

  @pytest.mark.parametrize("capture_group_count", [1, 2, 3])
  def test_generated_validator__is_cached(
      self,
      capture_group_count: int,
  ) -> None:
    validator1 = create_validator_regex_with_n_capture_groups(
        capture_group_count
    )
    validator2 = create_validator_regex_with_n_capture_groups(
        capture_group_count
    )

    assert validator1 == validator2

  @pytest.mark.parametrize(
      "value,capture_group_count", [
          ("1 capture (group)", 1),
          ("2 (capture) (groups)", 2),
          ("(3) (capture) (groups)", 3),
      ]
  )
  def test_generated_validator__matching_group_count__raises_no_exception(
      self,
      value: str,
      capture_group_count: int,
  ) -> None:
    validator = create_validator_regex_with_n_capture_groups(
        capture_group_count
    )

    validator(value)

  @pytest.mark.parametrize(
      "value,capture_group_count", [
          ("1 capture (group)", 3),
          ("2 (capture) (groups)", 1),
          ("(3) (capture) (groups)", 2),
      ]
  )
  def test_generated_validator__non_matching_group_count__raises_exception(
      self,
      value: str,
      capture_group_count: int,
  ) -> None:
    validator = create_validator_regex_with_n_capture_groups(
        capture_group_count
    )

    with pytest.raises(ValidationError) as exc:
      validator(value)

    assert str(exc.value.args[0]) == \
         (
             VALIDATION_ERROR_PREFIX +
             VALIDATION_ERROR_CAPTURE_GROUP_COUNT % capture_group_count
         )

  @pytest.mark.parametrize(
      "value,capture_group_count", [
          ("unbalanced capture group)", 1),
          ("*invalid wildcard", 2),
          ("[invalid character range", 3),
      ]
  )
  def test_generated_validator__uncompilable_regex__raises_exception(
      self,
      value: str,
      capture_group_count: int,
  ) -> None:
    validator = create_validator_regex_with_n_capture_groups(
        capture_group_count
    )

    with pytest.raises(ValidationError) as exc:
      validator(value)

    assert str(exc.value.args[0]).startswith(VALIDATION_ERROR_PREFIX)
