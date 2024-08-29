"""Fixtures for building Franchise models."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from stores.models.factories.franchise import FranchiseFactory

if TYPE_CHECKING:
  from stores.models import Franchise


@pytest.fixture
def franchise() -> Franchise:
  return FranchiseFactory.create()
