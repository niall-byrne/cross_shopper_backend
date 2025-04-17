"""Test the UniqueTogetherModelBatchFactory class."""

import random
from typing import Any
from unittest import mock

from utilities.models.generators.unique_together import (
    ConstraintDefinition,
    UniqueTogetherModelBatchFactory,
)


class TestUniqueTogetherModelBatchFactory:

  def assert_is_unique(self, called_kwargs: list[dict[str, Any]]) -> None:
    unique_argument_sets = []

    for kwargs in called_kwargs:
      assert kwargs not in unique_argument_sets
      unique_argument_sets.append(kwargs)

  def test_two_constraints(self) -> None:
    mock_factory = mock.Mock()

    factory = UniqueTogetherModelBatchFactory(
        model_factory=mock_factory,
        unique_together_constraint=(
            ConstraintDefinition(
                field_name="field_one",
                fn=lambda _: random.choice([True, False, None]),
            ),
            ConstraintDefinition(
                field_name="field_two",
                fn=lambda _: random.choice([True, False, None]),
            ),
        ),
        keyword="1",
    )

    factory.create_batch(9)

    self.assert_is_unique(
        [call.kwargs for call in mock_factory.create.mock_calls]
    )

  def test_three_constraints(self) -> None:
    mock_factory = mock.Mock()

    factory = UniqueTogetherModelBatchFactory(
        model_factory=mock_factory,
        unique_together_constraint=(
            ConstraintDefinition(
                field_name="field_one",
                fn=lambda _: random.choice([True, False, None]),
            ),
            ConstraintDefinition(
                field_name="field_two",
                fn=lambda _: random.choice([True, False, None]),
            ),
            ConstraintDefinition(
                field_name="field_three",
                fn=lambda _: random.choice([True, False, None]),
            ),
        ),
        keyword="1",
    )

    factory.create_batch(27)

    self.assert_is_unique(
        [call.kwargs for call in mock_factory.create.mock_calls]
    )
