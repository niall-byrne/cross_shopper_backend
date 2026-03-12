"""Test the Price model."""
from __future__ import annotations

import decimal
from typing import TYPE_CHECKING

import pytest
from django.core.exceptions import ValidationError
from freezegun import freeze_time
from pricing.models import Price
from pricing.models.defaults import default_pricing_week, default_pricing_year

if TYPE_CHECKING:
  from pricing.models.fixtures.pricing import AliasCreateLast52PriceBatch


@pytest.mark.django_db
class TestPrice:

  def test_initialize__defaults__attributes(
      self,
      price_today: Price,
  ) -> None:
    assert price_today.week == default_pricing_week.default_pricing_week()
    assert price_today.year == default_pricing_year.default_pricing_year()

  def test_constraint__unique_together(self, price: Price) -> None:
    price2 = Price(
        amount=price.amount,
        item=price.item,
        store=price.store,
        week=price.week,
        year=price.year,
    )

    with pytest.raises(ValidationError) as exc:
      price2.save()

    assert str(exc.value) == str(
        {
            "__all__":
                [
                    "Price with this Item, Store, Week and Year "
                    "already exists."
                ]
        }
    )

  def test_str__returns_correct_value(
      self,
      price: Price,
  ) -> None:
    assert str(price) == (
        f"{price.item.name_full}: "
        f"{price.store.franchise.name}, {price.store.address}, "
        f"Week {price.week} of {price.year}: {price.amount}"
    )

  @freeze_time("2035-1-1")
  def test_last_52_weeks_average__with_pricing__returns_minimum_value(
      self,
      create_last_52_price_batch: AliasCreateLast52PriceBatch,
  ) -> None:
    last_52_price_batch = create_last_52_price_batch()
    avg_price = (
        sum([price.amount for price in last_52_price_batch]) /
        decimal.Decimal(len(last_52_price_batch))
    ).quantize(
        decimal.Decimal(".01"),
        rounding=decimal.ROUND_HALF_UP,
    )
    model_object = last_52_price_batch[0]

    assert model_object.last_52_weeks_average == avg_price

  @freeze_time("2035-1-1")
  def test_last_52_weeks_average__with_no_pricing__returns_none(
      self,
      price_today: Price,
  ) -> None:
    assert price_today.last_52_weeks_average is None

  @freeze_time("2035-1-1")
  def test_last_52_weeks_avg__is_cached(
      self,
      create_last_52_price_batch: AliasCreateLast52PriceBatch,
  ) -> None:
    last_52_price_batch = create_last_52_price_batch()
    model_object = last_52_price_batch[0]
    cached_value = model_object.last_52_weeks_average
    for pricing in last_52_price_batch:
      pricing.amount = decimal.Decimal("0.01")
      pricing.save()

    assert model_object.last_52_weeks_average == cached_value

  @freeze_time("2035-1-1")
  def test_last_52_weeks_high__with_pricing__returns_maximum_value(
      self,
      create_last_52_price_batch: AliasCreateLast52PriceBatch,
  ) -> None:
    last_52_price_batch = create_last_52_price_batch()
    max_price = max([price.amount for price in last_52_price_batch])
    model_object = last_52_price_batch[0]

    assert model_object.last_52_weeks_high == max_price

  @freeze_time("2035-1-1")
  def test_last_52_weeks_high__with_no_pricing__returns_none(
      self,
      price_today: Price,
  ) -> None:
    assert price_today.last_52_weeks_high is None

  @freeze_time("2035-1-1")
  def test_last_52_weeks_high__is_cached(
      self,
      create_last_52_price_batch: AliasCreateLast52PriceBatch,
  ) -> None:
    last_52_price_batch = create_last_52_price_batch()
    max_price = max([price.amount for price in last_52_price_batch])
    offset_for_caching_test = 1
    model_object = last_52_price_batch[0]
    cached_value = model_object.last_52_weeks_high
    model_object.amount = max_price + offset_for_caching_test
    model_object.save()

    assert model_object.last_52_weeks_high == cached_value

  @freeze_time("2035-1-1")
  def test_last_52_weeks_low__with_pricing__returns_minimum_value(
      self,
      create_last_52_price_batch: AliasCreateLast52PriceBatch,
  ) -> None:
    last_52_price_batch = create_last_52_price_batch()
    min_price = min([price.amount for price in last_52_price_batch])
    model_object = last_52_price_batch[0]

    assert model_object.last_52_weeks_low == min_price

  @freeze_time("2035-1-1")
  def test_last_52_weeks_low__with_no_pricing__returns_zero(
      self,
      price_today: Price,
  ) -> None:
    assert price_today.last_52_weeks_low is None

  @freeze_time("2035-1-1")
  def test_last_52_weeks_low__is_cached(
      self,
      create_last_52_price_batch: AliasCreateLast52PriceBatch,
  ) -> None:
    last_52_price_batch = create_last_52_price_batch()
    min_price = min([price.amount for price in last_52_price_batch])
    offset_for_caching_test = decimal.Decimal("0.01")
    model_object = last_52_price_batch[0]
    cached_value = model_object.last_52_weeks_low
    model_object.amount = min_price - offset_for_caching_test
    model_object.save()

    assert model_object.last_52_weeks_low == cached_value
