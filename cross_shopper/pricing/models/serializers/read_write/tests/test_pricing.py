"""Test the PricingSerializerRW class."""
from __future__ import annotations

import decimal
from typing import TYPE_CHECKING

import pytest
from pricing.models import Price
from pricing.models.defaults import default_pricing_week, default_pricing_year
from pricing.models.serializers.read_write.pricing import PricingSerializerRW

if TYPE_CHECKING:
  from items.models import Item
  from stores.models import Store


@pytest.mark.django_db
class TestPricingSerializeRW:

  def test_serialization__correct_representation(
      self,
      price: Price,
  ) -> None:
    serialized = PricingSerializerRW(price)

    assert serialized.data == {
        "id": price.pk,
        "amount": str(price.amount),
        "item": price.item.pk,
        "store": price.store.pk,
        "week": price.week,
        "year": price.year,
    }

  def test_deserialization__valid_input__non_existent__correct_model(
      self,
      item: Item,
      store: Store,
  ) -> None:
    pricing_data: dict[str, str | int] = {
        "amount": "1000.01",
        "item": item.pk,
        "store": store.pk,
    }

    serialized = PricingSerializerRW(data=pricing_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.amount == decimal.Decimal(pricing_data["amount"])
    assert instance.item == item
    assert instance.store == store
    assert instance.week == default_pricing_week.default_pricing_week()
    assert instance.year == default_pricing_year.default_pricing_year()

  def test_deserialization__valid_input__existent__upserts_model(
      self,
      item: Item,
      store: Store,
  ) -> None:
    pricing_data: dict[str, str | int] = {
        "amount": "1000.01",
        "item": item.pk,
        "store": store.pk,
    }
    instance = Price(
        amount="500.00",
        item=item,
        store=store,
    )
    instance.save()

    serialized = PricingSerializerRW(data=pricing_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.pk == serialized.data["id"]
    assert instance.amount == decimal.Decimal(pricing_data["amount"])
