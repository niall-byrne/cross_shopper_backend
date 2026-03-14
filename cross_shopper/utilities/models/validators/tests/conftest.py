"""Fixtures for the MultiFieldValidator tests."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock

import pytest
from django.db.models import Model
from utilities.models.validators.multi_field_validator import (
    MultiFieldValidator,
)


@dataclass
class ConcreteMultiFieldValidator(MultiFieldValidator["Model"]):
  """A concrete implementation of MultiFieldValidator for testing."""

  extra_info: str = "extra"

  def is_model_valid(self, instance: Model) -> bool:
    """Evaluate the model validation."""
    return True  # no cover


@pytest.fixture
def concrete_validator() -> ConcreteMultiFieldValidator:
  """Fixture for a concrete validator."""
  return ConcreteMultiFieldValidator(
      model_fields=["field1", "field2"],
      error_message="Error for {model_fields} with {extra_info}",
  )


@pytest.fixture
def mocked_model() -> MagicMock:
  """Fixture for a mocked Django model."""
  model = MagicMock(spec=Model)
  model.field1 = "value1"
  model.nested = MagicMock(spec=Model)
  model.nested.field2 = "value2"
  return model


@pytest.fixture
def mocked_serialized_model_full() -> dict[str, Any]:
  """Fixture for mocked fully serialized model."""
  return {
      "field1": "value1",
      "nested": {
          "field2": "value2"
      },
  }


@pytest.fixture
def mocked_serialized_model_partial(mocked_model: MagicMock,) -> dict[str, Any]:
  """Fixture for mocked partially serialized model."""
  return {
      "nested": {
          "model": mocked_model
      },
  }
