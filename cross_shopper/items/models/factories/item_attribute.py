"""Factories for ItemAttribute model instances."""
from __future__ import annotations

from typing import TYPE_CHECKING

import factory
from items.models.factories.attribute import AttributeFactory
from items.models.factories.item import ItemFactory

if TYPE_CHECKING:
  from items.models import (
      Attribute,
      Item,
      ItemAttribute,  # noqa: F401
  )
  from .typing import AliasSubFactory


class ItemAttributeFactory(factory.django.DjangoModelFactory["ItemAttribute"]):
  item: AliasSubFactory[Item] = factory.SubFactory(ItemFactory)
  attribute: AliasSubFactory[Attribute] = factory.SubFactory(AttributeFactory)

  class Meta:
    model = "items.ItemAttribute"
