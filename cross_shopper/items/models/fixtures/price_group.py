"""Fixtures for building PriceGroup models."""

import pytest
from items.models import PriceGroup
from items.models.factories.price_group import PriceGroupFactory


@pytest.fixture
def price_group() -> "PriceGroup":
  return PriceGroupFactory.create()
