"""Fixtures for building ItemAttribute models."""

from typing import TYPE_CHECKING

import pytest
from items.models import PriceGroupAttribute
from items.models.factories.price_group_attribute import (
    PriceGroupAttributeFactory,
)

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet


@pytest.fixture
def price_group_attribute() -> "PriceGroupAttribute":
  return PriceGroupAttributeFactory.create()


@pytest.fixture
def price_group_attribute_batch() -> "QuerySet[PriceGroupAttribute]":
  item_attributes = PriceGroupAttributeFactory.create_batch(size=10)
  return PriceGroupAttribute.objects.filter(
      id__in=[instance.pk for instance in item_attributes]
  )
