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
      report_context_2024: Dict,
  ) -> None:
    prices = Price.objects.all()
    serializer = ReportSummaryCurrentItemPriceSerializerRO(
        report_with_2024_prices.item.all()[0],
        context=report_context_2024,
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
      report_context_no_prices: Dict,
  ) -> None:
    serializer = ReportSummaryCurrentItemPriceSerializerRO(
        report.item.all()[0],
        context=report_context_no_prices,
    )

    data = serializer.data

    assert data == {
        'average': None,
        'best': None,
        'per_store': {
            str(store.pk): None for store in report.store.all()
        },
    }

  def test_repr__specified_context__returns_correct_string(
      self,
      report: Report,
      report_context_2024: Dict,
  ) -> None:
    serializer = ReportSummaryCurrentItemPriceSerializerRO(
        report.item.all()[0],
        context=report_context_2024,
    )

    serializer_repr = repr(serializer)

    assert serializer_repr == ":".join(
        [
            repr(report_context_2024['week']),
            repr(report_context_2024['year']),
            repr(report_context_2024['report']),
            repr(ReportSummaryCurrentItemPriceSerializerRO),
        ]
    )

  def test_get_average__multiple_instances__same_context__shares_cache(
      self,
      report_with_2024_prices: Report,
      report_context_2024: Dict,
      report_summary_mocked_get_per_store: mock.Mock,
  ) -> None:
    item = report_with_2024_prices.item.all()[0]
    serializer1 = ReportSummaryCurrentItemPriceSerializerRO(
        item,
        context=report_context_2024,
    )
    serializer2 = ReportSummaryCurrentItemPriceSerializerRO(
        item,
        context=report_context_2024,
    )

    res1 = serializer1.get_average(item)
    res2 = serializer2.get_average(item)

    assert res1 == res2
    assert report_summary_mocked_get_per_store.call_count == 1

  def test_get_average__multiple_instances__different_context__isolated_cache(
      self,
      report_with_2024_prices: Report,
      report_context_2024: Dict,
      report_context_2024_alternate: Dict,
      report_summary_mocked_get_per_store: mock.Mock,
  ) -> None:
    item = report_with_2024_prices.item.all()[0]
    serializer1 = ReportSummaryCurrentItemPriceSerializerRO(
        item,
        context=report_context_2024,
    )
    serializer2 = ReportSummaryCurrentItemPriceSerializerRO(
        item,
        context=report_context_2024_alternate,
    )

    serializer1.get_average(item)
    serializer2.get_average(item)

    assert report_summary_mocked_get_per_store.call_count == 2
