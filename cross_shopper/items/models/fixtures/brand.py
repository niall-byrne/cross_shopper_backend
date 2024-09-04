"""Fixtures for building Brand models."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from items.models.factories.brand import BrandFactory

if TYPE_CHECKING:
  from items.models import Brand


@pytest.fixture
def brand() -> Brand:
  return BrandFactory.create()
