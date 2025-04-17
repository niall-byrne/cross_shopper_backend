"""Factories for Price model instances."""

from typing import TYPE_CHECKING

import factory
from factory import fuzzy
from items.models.factories.item import ItemFactory
from stores.models.factories.store import StoreFactory

if TYPE_CHECKING:  # no cover
  from decimal import Decimal

  from items.models import Item  # noqa: F401
  from pricing.models import Price  # noqa: F401
  from stores.models import Store  # noqa: F401
  from .typing import AliasFaker, AliasFuzzyChoice, AliasSubFactory


class TodayPriceFactory(factory.django.DjangoModelFactory["Price"]):
  amount: "AliasFaker[Decimal]" = factory.Faker(
      "pydecimal",
      left_digits=4,
      right_digits=2,
      min_value=0.01,
  )
  item: "AliasSubFactory[Item]" = factory.SubFactory(ItemFactory)
  store: "AliasSubFactory[Store]" = factory.SubFactory(StoreFactory)

  class Meta:
    model = "pricing.Price"


class PriceFactory(TodayPriceFactory):
  week: "AliasFuzzyChoice[int]" = fuzzy.FuzzyChoice(range(1, 52))
  year: "AliasFuzzyChoice[int]" = fuzzy.FuzzyChoice(range(2024, 2050))
