"""Tests for the ReportSummaryCurrentItemPriceSerializer."""
from __future__ import annotations

import decimal
from typing import TYPE_CHECKING

import pytest
from django.db.models import Avg, Min
from pricing.models import Price
from reports.models.serializers.report_summary.item_price_current import (
    ReportSummaryCurrentItemPriceSerializer,
)

if TYPE_CHECKING:
  from reports.models.report import Report


@pytest.mark.django_db
class TestReportSummaryCurrentItemPriceSerializer:

  def test_serialization__specified_item__returns_correct_representation(
      self,
      report_with_2024_prices: Report,
  ) -> None:
    prices = Price.objects.all()

    serializer = ReportSummaryCurrentItemPriceSerializer(
        report_with_2024_prices.item.all()[0],
        context={
            "report": report_with_2024_prices,
            "year": 2024,
            "week": 1,
        },
    )

    expected_per_store: dict[str, str | None] = {}
    for store in report_with_2024_prices.store.all():
      price = prices.filter(store=store).first()
      if price:
        expected_per_store[str(store.pk)] = str(price.amount)

    assert serializer.data == {
        "per_store":
            expected_per_store,
        "best":
            str(
                prices.aggregate(Min("amount"))["amount__min"].quantize(
                    decimal.Decimal(".00")
                )
            ),
        "average":
            str(
                prices.aggregate(Avg("amount"))["amount__avg"].quantize(
                    decimal.Decimal(".00")
                )
            ),
    }

  def test_serialization__no_prices__returns_none(
      self,
      report: Report,
  ) -> None:
    serializer = ReportSummaryCurrentItemPriceSerializer(
        report.item.all()[0],
        context={
            "report": report,
            "year": 2024,
            "week": 1,
        },
    )

    assert serializer.data == {
        "average": None,
        "best": None,
        "per_store": {
            str(store.pk): None for store in report.store.all()
        },
    }
