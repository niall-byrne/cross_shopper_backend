"""Fixtures for the MultiFieldValidator tests."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest
from utilities.models.validators.multi_field_validator import (
    MultiFieldValidator,
)

if TYPE_CHECKING:  # no cover
  from typing import Any, Dict
  from unittest.mock import MagicMock

  from django.db.models import Model


@dataclass
class ConcreteMultiFieldValidator(MultiFieldValidator["Model"]):
  """A concrete implementation of MultiFieldValidator for testing."""

  extra_info: str = "extra"

  def is_model_valid(self, instance: "Model") -> bool:
    """Evaluate the model validation."""
    return True  # pragma: no cover


@pytest.fixture
def concrete_validator() -> "ConcreteMultiFieldValidator":
  """Fixture for a concrete validator."""
  return ConcreteMultiFieldValidator(
      model_fields=["field1", "field2"],
      error_message="Error for {model_fields} with {extra_info}",
  )


@pytest.fixture
def mocked_model() -> "MagicMock":
  """Fixture for a mocked Django model."""
  from unittest.mock import MagicMock

  from django.db.models import Model
  model = MagicMock(spec=Model)
  model.field1 = "value1"
  model.nested = MagicMock()
  model.nested.field2 = "value2"
  return model


@pytest.fixture
def mocked_serialized_data_full() -> "Dict[str, Any]":
  """Fixture for mocked fully serialized data."""
  return {
      "field1": "value1",
      "nested": {
          "field2": "value2"
      },
  }


@pytest.fixture
def mocked_serialized_data_partial(mocked_model: "MagicMock") -> "Dict[str, Any]":
  """Fixture for mocked partially serialized data."""
  return {
      "nested": {
          "model": mocked_model
      },
  }
