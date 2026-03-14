"""Factories for ItemAttribute model instances."""
from __future__ import annotations

from typing import TYPE_CHECKING

import factory
from items.models.factories.attribute import AttributeFactory
from items.models.factories.price_group import PriceGroupFactory

if TYPE_CHECKING:
  from items.models import (
      Attribute,
      PriceGroup,
      PriceGroupAttribute,  # noqa: F401
  )
  from .typing import AliasSubFactory


class PriceGroupAttributeFactory(
    factory.django.DjangoModelFactory["PriceGroupAttribute"],
):
  price_group: AliasSubFactory[PriceGroup] = factory.SubFactory(
      PriceGroupFactory,
  )
  attribute: AliasSubFactory[Attribute] = factory.SubFactory(AttributeFactory,)

  class Meta:
    model = "items.PriceGroupAttribute"
