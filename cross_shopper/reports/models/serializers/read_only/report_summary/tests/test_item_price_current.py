"""Tests for the ReportSummaryCurrentItemPriceSerializerRO."""

import decimal
from typing import Dict, Optional

import pytest
from django.db.models import Avg, Min
from pricing.models import Price
from reports.models.report import Report
from reports.models.serializers.read_only.report_summary.\
  item_price_current import (
    ReportSummaryCurrentItemPriceSerializerRO,
)


@pytest.mark.django_db
class TestReportSummaryCurrentItemPriceSerializerRO:
  """Tests for the ReportSummaryCurrentItemPriceSerializerRO."""

  def test_serialization__specified_item__returns_correct_representation(
      self,
      report_with_2024_prices: "Report",
  ) -> None:
    prices = Price.objects.all()

    serializer = ReportSummaryCurrentItemPriceSerializerRO(
        report_with_2024_prices.item.all()[0],
        context={
            'report': report_with_2024_prices,
            'year': 2024,
            'week': 1,
        },
    )

    expected_per_store: Dict[str, Optional[str]] = {}
    for store in report_with_2024_prices.store.all():
      price = prices.filter(store=store).first()
      if price:
        expected_per_store[str(store.pk)] = str(price.amount)

    assert serializer.data == {
        'per_store':
            expected_per_store,
        'best':
            str(
                prices.aggregate(Min('amount'))['amount__min'].quantize(
                    decimal.Decimal('.00')
                )
            ),
        'average':
            str(
                prices.aggregate(Avg('amount'))['amount__avg'].quantize(
                    decimal.Decimal('.00')
                )
            ),
    }

  def test_serialization__no_prices__returns_none(
      self,
      report: "Report",
  ) -> None:
    serializer = ReportSummaryCurrentItemPriceSerializerRO(
        report.item.all()[0],
        context={
            'report': report,
            'year': 2024,
            'week': 1,
        },
    )

    assert serializer.data == {
        'average': None,
        'best': None,
        'per_store': {
            str(store.pk): None for store in report.store.all()
        },
    }
