"""An aggregate model manager for last 52 week item pricing across stores."""
from __future__ import annotations

import decimal
from datetime import datetime
from typing import TYPE_CHECKING, Sequence, cast

from django.db import models
from django.db.models import Avg, Max, Min
from pricing.models.pricing import default_pricing_week, default_pricing_year

if TYPE_CHECKING:
  from items.models import Item
  from pricing.models import Price  # noqa: F401
  from stores.models import Store


class AggregateLast52WeeksManager(models.Manager["Price"]):
  """An aggregate model manager for last 52 week item pricing across stores."""

  def get_last_52_weeks(
      self,
      item: Item,
      store: models.QuerySet[Store] | Sequence[Store],
  ) -> models.QuerySet[Price]:
    """Return the given item's last 52 weeks of pricing at the given stores."""
    current_year = default_pricing_year()
    current_week = default_pricing_week()
    last_year_remainder_weeks = 52 - current_week
    last_year_total_weeks = datetime(
        year=current_year - 1,
        month=12,
        day=31,
    ).isocalendar().week

    current_year_pricing = self.get_queryset().filter(
        item=item,
        store__in=store,
        year=current_year,
        week__lte=current_week,
    )

    if last_year_remainder_weeks <= 0:
      return current_year_pricing

    last_year_pricing = self.get_queryset().filter(
        item=item,
        store__in=store,
        year=current_year - 1,
        week__gte=last_year_total_weeks - last_year_remainder_weeks,
    )

    return current_year_pricing | last_year_pricing

  def average(
      self,
      item: Item,
      store: models.QuerySet[Store],
  ) -> decimal.Decimal | None:
    """Calculate the average price for the given item at the given stores."""
    pricing = self.get_last_52_weeks(item, store)

    if not pricing:
      return None

    return cast(
        "decimal.Decimal",
        pricing.aggregate(Avg("amount"))["amount__avg"].quantize(
            decimal.Decimal(".01"),
            rounding=decimal.ROUND_HALF_UP,
        )
    )

  def high(
      self,
      item: Item,
      store: models.QuerySet[Store],
  ) -> decimal.Decimal | None:
    """Calculate the highest price for the given item at the given stores."""
    pricing = self.get_last_52_weeks(item, store)

    if not pricing:
      return None

    return cast(
        "decimal.Decimal",
        pricing.aggregate(Max("amount"),)["amount__max"].quantize(
            decimal.Decimal(".00")
        )
    )

  def low(
      self,
      item: Item,
      store: models.QuerySet[Store],
  ) -> decimal.Decimal | None:
    """Calculate the lowest price for the given item at the given stores."""
    pricing = self.get_last_52_weeks(item, store)

    if not pricing:
      return None

    return cast(
        "decimal.Decimal",
        pricing.aggregate(Min("amount"),)["amount__min"].quantize(
            decimal.Decimal(".00")
        )
    )
