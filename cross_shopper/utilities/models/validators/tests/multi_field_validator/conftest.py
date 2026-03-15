"""Fixtures for the MultiFieldValidator tests."""

from typing import Any
from unittest.mock import MagicMock

import pytest
from django.db.models import Model
from cross_shopper.utilities.models.validators.tests.multi_field_validator.helpers import (
    ConcreteMultiFieldValidator,
)


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
  model.nested = MagicMock()
  model.nested.field2 = "value2"
  return model


@pytest.fixture
def mocked_serializer_data() -> dict[str, Any]:
  """Fixture for mocked serializer data."""
  return {
      "field1": "value1",
      "nested": {
          "field2": "value2"
      },
  }
