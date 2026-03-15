"""Fixtures for testing MultiFieldValidator."""

from unittest.mock import Mock

import pytest
from utilities.models.validators.tests.__helper__ import (
    ConcreteMultiFieldValidator,
)


@pytest.fixture
def mocked_model_instance() -> Mock:
  """Mocked Django model instance."""
  return Mock()


@pytest.fixture
def multi_field_validator() -> ConcreteMultiFieldValidator:
  """Concrete MultiFieldValidator instance."""
  return ConcreteMultiFieldValidator(
      model_fields=["field1", "field2"],
      error_message="Error in {model_fields}",
  )
