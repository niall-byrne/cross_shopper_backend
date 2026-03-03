"""Tests for the ReportSummaryCurrentItemPriceSerializerRO."""

import decimal
from typing import Dict, Optional
from unittest import mock

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

  def test_serialization__specified_item__returns_correct_representation(
      self,
      report_with_2024_prices: Report,
      report_2024_context: Dict,
  ) -> None:
    prices = Price.objects.all()
    serializer = ReportSummaryCurrentItemPriceSerializerRO(
        report_with_2024_prices.item.all()[0],
        context=report_2024_context,
    )
    expected_per_store: Dict[str, Optional[str]] = {}
    for store in report_with_2024_prices.store.all():
      price = prices.filter(store=store).first()
      if price:
        expected_per_store[str(store.pk)] = str(price.amount)

    data = serializer.data

    assert data == {
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
      report: Report,
      report_no_prices_context: Dict,
  ) -> None:
    serializer = ReportSummaryCurrentItemPriceSerializerRO(
        report.item.all()[0],
        context=report_no_prices_context,
    )

    data = serializer.data

    assert data == {
        'average': None,
        'best': None,
        'per_store': {
            str(store.pk): None for store in report.store.all()
        },
    }

  def test___repr____specified_context__returns_correct_string(
      self,
      report: Report,
      report_2024_context: Dict,
  ) -> None:
    serializer = ReportSummaryCurrentItemPriceSerializerRO(
        report.item.all()[0],
        context=report_2024_context,
    )

    serializer_repr = repr(serializer)

    assert serializer_repr == ":".join(
        [
            repr(report_2024_context['week']),
            repr(report_2024_context['year']),
            repr(report_2024_context['report']),
            repr(ReportSummaryCurrentItemPriceSerializerRO),
        ]
    )

  def test_get_average__multiple_instances_same_context__shares_cache(
      self,
      report_with_2024_prices: Report,
      report_2024_context: Dict,
  ) -> None:
    item = report_with_2024_prices.item.all()[0]
    serializer1 = ReportSummaryCurrentItemPriceSerializerRO(
        item,
        context=report_2024_context,
    )
    serializer2 = ReportSummaryCurrentItemPriceSerializerRO(
        item,
        context=report_2024_context,
    )

    with mock.patch.object(
        ReportSummaryCurrentItemPriceSerializerRO,
        'get_per_store',
        wraps=serializer1.get_per_store,
    ) as mock_get_per_store:
      mock_get_per_store.__name__ = "get_per_store_mocked"
      res1 = serializer1.get_average(item)
      res2 = serializer2.get_average(item)

    assert res1 == res2
    assert mock_get_per_store.call_count == 1

  def test_get_average__multiple_instances_different_context__isolated_cache(
      self,
      report_with_2024_prices: Report,
      report_2024_context: Dict,
      report_2024_different_week_context: Dict,
  ) -> None:
    item = report_with_2024_prices.item.all()[0]
    serializer1 = ReportSummaryCurrentItemPriceSerializerRO(
        item,
        context=report_2024_context,
    )
    serializer2 = ReportSummaryCurrentItemPriceSerializerRO(
        item,
        context=report_2024_different_week_context,
    )

    with mock.patch.object(
        ReportSummaryCurrentItemPriceSerializerRO,
        'get_per_store',
        wraps=serializer1.get_per_store,
    ) as mock_get_per_store:
      mock_get_per_store.__name__ = "get_per_store_mocked_isolated"
      serializer1.get_average(item)
      serializer2.get_average(item)

    assert mock_get_per_store.call_count == 2
