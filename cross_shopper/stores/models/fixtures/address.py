"""Fixtures for building Address models."""

from typing import TYPE_CHECKING

import pytest
from stores.models.factories.address import AddressFactory

if TYPE_CHECKING:  # no cover
  from address.models import Address


@pytest.fixture
def address() -> "Address":
  return AddressFactory.create()
