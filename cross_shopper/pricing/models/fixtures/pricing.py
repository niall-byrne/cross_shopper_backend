"""Fixtures for building Price models."""
from __future__ import annotations

import random
from datetime import datetime
from typing import TYPE_CHECKING, Callable

import pytest
from items.models.factories.item import ItemFactory
from pricing.models.defaults.default_pricing_week import default_pricing_week
from pricing.models.defaults.default_pricing_year import default_pricing_year
from pricing.models.factories.pricing import PriceFactory, TodayPriceFactory
from stores.models.factories.store import StoreFactory
from utilities.models.generators.unique_together import (
    ConstraintDefinition,
    UniqueTogetherModelBatchFactory,
)

if TYPE_CHECKING:
  from pricing.models import Price
  from reports.models import Report
  from stores.models import Store

AliasPriceBatchFactory = Callable[[int], list["Price"]]
AliasPriceVaryStoreBatchFactory = Callable[[int, "Store"], list["Price"]]
AliasCreateLast52PriceBatch = Callable[[], list["Price"]]
AliasCreateLast52PriceBatchFromReport = Callable[["Report"], list["Price"]]


def filter_to_last_52_weeks(price_batch: list[Price]) -> list[Price]:
  filtered_prices: list[Price] = []

  current_year = default_pricing_year()
  current_week = default_pricing_week()
  last_year_remainder_weeks = 52 - current_week
  last_year_total_weeks = datetime(current_year - 1, 12, 31).isocalendar().week

  for price in price_batch:
    if price.year == current_year and price.week <= current_week:
      filtered_prices.append(price)

  if last_year_remainder_weeks <= 0:
    return filtered_prices

  for price in price_batch:
    if (
        price.year == current_year - 1 and  # noqa: W504
        price.week >= last_year_total_weeks - last_year_remainder_weeks
    ):
      filtered_prices.append(price)

  return filtered_prices


@pytest.fixture
def price() -> Price:
  return PriceFactory.create()


@pytest.fixture
def price_today() -> Price:
  return TodayPriceFactory.create()


@pytest.fixture
def create_last_52_price_batch() -> AliasCreateLast52PriceBatch:

  def create() -> list[Price]:
    current_year = default_pricing_year()

    factory = UniqueTogetherModelBatchFactory(
        model_factory=PriceFactory,
        unique_together_constraint=(
            ConstraintDefinition(
                field_name="week",
                fn=lambda _: random.choice(range(1, 52)),
            ),
            ConstraintDefinition(
                field_name="year",
                fn=lambda _: random.
                choice(range(current_year - 2, current_year + 1)),
            ),
        ),
        item=ItemFactory.create(),
        store=StoreFactory.create(),
    )

    price_batch: list[Price] = factory.create_batch(60)
    return filter_to_last_52_weeks(price_batch)

  return create


@pytest.fixture
def create_last_52_price_batch_from_report(
) -> AliasCreateLast52PriceBatchFromReport:

  def create(report: Report) -> list[Price]:
    current_year = default_pricing_year()
    stores = list(report.store.all())
    item = report.item.all()[0]

    factory = UniqueTogetherModelBatchFactory(
        model_factory=PriceFactory,
        unique_together_constraint=(
            ConstraintDefinition(
                field_name="week",
                fn=lambda _: random.choice(range(1, 53)),
            ),
            ConstraintDefinition(
                field_name="year",
                fn=lambda _: random.
                choice(range(current_year - 2, current_year + 1)),
            ),
        ),
        store=random.choice(stores)
    )

    price_batch: list[Price] = factory.create_batch(60, item=item)
    return filter_to_last_52_weeks(price_batch)

  return create
