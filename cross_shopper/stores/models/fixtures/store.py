"""Fixtures for building Store models."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from stores.models.factories.store import StoreFactory

if TYPE_CHECKING:
  from stores.models import Store


@pytest.fixture
def store() -> Store:
  return StoreFactory.create()
