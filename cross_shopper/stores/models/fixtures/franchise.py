"""Fixtures for building Franchise models."""

from typing import TYPE_CHECKING

import pytest
from stores.models.factories.franchise import FranchiseFactory

if TYPE_CHECKING:  # no cover
  from stores.models import Franchise


@pytest.fixture
def franchise() -> "Franchise":
  return FranchiseFactory.create()
