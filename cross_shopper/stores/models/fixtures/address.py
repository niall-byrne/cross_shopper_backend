"""Fixtures for building Address models."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from stores.models.factories.address import AddressFactory

if TYPE_CHECKING:
  from address.models import Address


@pytest.fixture
def address() -> Address:
  return AddressFactory.create()
