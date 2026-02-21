"""Fixtures for building ErrorType models."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from errors.models.factories.error_type import ErrorTypeFactory

if TYPE_CHECKING:
  from errors.models import ErrorType


@pytest.fixture
def error_type() -> ErrorType:
  return ErrorTypeFactory.create()
