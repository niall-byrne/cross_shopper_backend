"""Fixtures for building ErrorType models."""

from typing import TYPE_CHECKING

import pytest
from errors.models.factories.error_type import ErrorTypeFactory

if TYPE_CHECKING:  # no cover
  from errors.models import ErrorType


@pytest.fixture
def error_type() -> "ErrorType":
  return ErrorTypeFactory.create()
