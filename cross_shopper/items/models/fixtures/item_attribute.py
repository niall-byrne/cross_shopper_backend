"""Fixtures for building ItemAttribute models."""

from typing import TYPE_CHECKING

import pytest
from items.models import ItemAttribute
from items.models.factories.item_attribute import ItemAttributeFactory

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet


@pytest.fixture
def item_attribute() -> "ItemAttribute":
  return ItemAttributeFactory.create()


@pytest.fixture
def item_attribute_batch() -> "QuerySet[ItemAttribute]":
  item_attributes = ItemAttributeFactory.create_batch(size=10)
  return ItemAttribute.objects.filter(
      id__in=[instance.pk for instance in item_attributes]
  )
