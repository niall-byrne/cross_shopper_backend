"""Fixtures for building Brand models."""

from typing import TYPE_CHECKING

import pytest
from items.models.factories.brand import BrandFactory

if TYPE_CHECKING:  # no cover
  from items.models import Brand


@pytest.fixture
def brand() -> "Brand":
  return BrandFactory.create()
