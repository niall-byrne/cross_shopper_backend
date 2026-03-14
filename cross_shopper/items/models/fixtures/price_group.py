"""Fixtures for building PriceGroup models."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from items.models.factories.price_group import PriceGroupFactory

if TYPE_CHECKING:
  from items.models import Attribute, PriceGroup


@pytest.fixture
def price_group(attribute: Attribute) -> PriceGroup:
  return PriceGroupFactory.create(attributes=[attribute])
