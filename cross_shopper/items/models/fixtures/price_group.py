"""Fixtures for building PriceGroup models."""

from typing import TYPE_CHECKING

import pytest
from items.models import PriceGroup
from items.models.factories.price_group import PriceGroupFactory

if TYPE_CHECKING:  # no cover
  from items.models import Attribute


@pytest.fixture
def price_group(attribute: "Attribute") -> "PriceGroup":
  return PriceGroupFactory.create(attributes=[attribute])
