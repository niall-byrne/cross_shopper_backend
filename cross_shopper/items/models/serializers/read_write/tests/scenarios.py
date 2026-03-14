"""Scenarios for the items app read/write serializer tests."""

from typing import TYPE_CHECKING, TypeVar

import pytest
from items.models.validators.item import model_level_validators

if TYPE_CHECKING:  # no cover
  from typing import Callable
  TestFunctionType = TypeVar('TestFunctionType', bound="Callable[..., None]")


def item_deserialization_validator_scenarios(  # noqa: D103
    func: "TestFunctionType",
) -> "TestFunctionType":
  func = pytest.mark.parametrize(
      "validator, parameters",
      (
          (
              model_level_validators[0],
              {
                  "is_organic": True
              },
          ), (
              model_level_validators[1],
              {
                  "is_non_gmo": True
              },
          ), (
              model_level_validators[2],
              {
                  "unit": "Invalid Unit"
              },
          )
      ),
  )(func)
  return func
