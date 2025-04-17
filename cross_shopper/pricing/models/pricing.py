"""Price model."""
from __future__ import annotations

import decimal
from typing import cast

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, Max, Min
from django.utils.functional import cached_property
from utilities.models.bases.model_base import ModelBase
from utilities.models.validators.greater_than_zero import (
    validator_greater_than_zero,
)
from .defaults.default_pricing_week import default_pricing_week
from .defaults.default_pricing_year import default_pricing_year
from .managers.last_52_weeks import AggregateLast52WeeksManager


class Price(
    ModelBase,
):
  DAY_OF_WEEK_FOR_PRICING = 3  # Thursday

  amount = models.DecimalField(
      decimal_places=2,
      max_digits=11,
      validators=[validator_greater_than_zero],
  )
  item = models.ForeignKey(
      "items.Item",
      on_delete=models.CASCADE,
  )
  store = models.ForeignKey(
      "stores.Store",
      on_delete=models.CASCADE,
  )
  week = models.IntegerField(
      default=default_pricing_week,
      validators=[
          MinValueValidator(1),
          MaxValueValidator(53),
      ]
  )
  year = models.IntegerField(
      default=default_pricing_year,
      validators=[
          MinValueValidator(2024),
          MaxValueValidator(2100),
      ]
  )

  aggregate_last_52_weeks = AggregateLast52WeeksManager()
  objects = models.Manager()

  class Meta:
    verbose_name_plural = "Pricing"
    unique_together = ("item", "store", "week", "year")

  def __str__(self) -> str:
    return (
        f"{self.item.full_name}: "
        f"{self.store.franchise.name}, {self.store.address}, "
        f"Week {self.week} of {self.year}: {self.amount}"
    )

  @cached_property
  def _last_52_weeks(self) -> models.QuerySet[Price]:
    return Price.aggregate_last_52_weeks.get_last_52_weeks(
        self.item,
        [self.store],
    ).order_by("id")

  @cached_property
  def last_52_weeks_average(self) -> decimal.Decimal | None:
    """Calculate the average item price for the past 52 weeks at this store."""
    if self._last_52_weeks.exists():
      return cast(
          "decimal.Decimal",
          self._last_52_weeks.aggregate(Avg("amount"))["amount__avg"].quantize(
              decimal.Decimal(".01"),
              rounding=decimal.ROUND_HALF_UP,
          )
      )

    return None

  @cached_property
  def last_52_weeks_high(self) -> decimal.Decimal | None:
    """Calculate the highest item price for the past 52 weeks at this store."""
    if self._last_52_weeks.exists():
      return cast(
          "decimal.Decimal",
          self._last_52_weeks.aggregate(Max("amount"))["amount__max"].quantize(
              decimal.Decimal(".00")
          )
      )

    return None

  @cached_property
  def last_52_weeks_low(self) -> decimal.Decimal | None:
    """Calculate the lowest item price for the past 52 weeks at this store."""
    if self._last_52_weeks.exists():
      return cast(
          "decimal.Decimal",
          self._last_52_weeks.aggregate(Min("amount"))["amount__min"].quantize(
              decimal.Decimal(".00")
          )
      )

    return None
