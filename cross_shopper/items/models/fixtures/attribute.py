"""Fixtures for building Attribute models."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from items.models import Attribute
from items.models.factories.attribute import AttributeFactory

if TYPE_CHECKING:
  from django.db.models import QuerySet


@pytest.fixture
def attribute() -> Attribute:
  return AttributeFactory.create()


@pytest.fixture
def attribute_alternate() -> Attribute:
  return AttributeFactory.create()


@pytest.fixture
def attribute_batch() -> QuerySet[Attribute]:
  attributes = AttributeFactory.create_batch(size=10)
  return Attribute.objects.filter(
      id__in=[instance.pk for instance in attributes]
  )
