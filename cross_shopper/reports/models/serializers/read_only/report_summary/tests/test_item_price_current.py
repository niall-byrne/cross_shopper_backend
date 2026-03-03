"""Tests for the ReportSummaryCurrentItemPriceSerializerRO."""

import decimal
from typing import TYPE_CHECKING

import pytest
from django.db.models import Avg, Min
from pricing.models import Price
from reports.models.report import Report
from reports.models.serializers.read_only.report_summary.\
  item_price_current import (
    ReportSummaryCurrentItemPriceSerializerRO,
)

if TYPE_CHECKING:  # no cover
  from typing import Any, Dict, Optional

  from reports.models.report import Report
  from .conftest import AliasSerializerMockCreator


@pytest.mark.django_db
class TestReportSummaryCurrentItemPriceSerializerRO:

  def test_serialization__specified_item__returns_correct_representation(
      self,
      report_with_2024_prices: "Report",
      report_context_2024: "Dict[str, Any]",
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
      report: "Report",
      report_context_no_prices: "Dict[str, Any]",
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
      report: "Report",
      report_context_2024: "Dict[str, Any]",
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

  @pytest.mark.parametrize("cached_method", (
      "average",
      "best",
  ))
  def test_cached_method__multiple_instances__same_context__shares_cache(
      self,
      report_with_2024_prices: "Report",
      report_context_2024: "Dict[str, Any]",
      create_mocked_rs_serializer_price_getter: "AliasSerializerMockCreator",
      cached_method: "str",
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
    mocked_method = create_mocked_rs_serializer_price_getter("per_store")

    res1 = getattr(serializer1, f"get_{cached_method}")(item)
    res2 = getattr(serializer2, f"get_{cached_method}")(item)

    assert res1 == res2
    assert mocked_method.call_count == 1

  @pytest.mark.parametrize("cached_method", (
      "average",
      "best",
  ))
  def test_cached_method__multiple_instances__different_context__isolated_cache(
      self,
      report_with_2024_prices: "Report",
      report_context_2024: "Dict[str, Any]",
      report_context_2024_alternate: "Dict[str, Any]",
      create_mocked_rs_serializer_price_getter: "AliasSerializerMockCreator",
      cached_method: "str",
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
    mocked_method = create_mocked_rs_serializer_price_getter("per_store")

    getattr(serializer1, f"get_{cached_method}")(item)
    getattr(serializer2, f"get_{cached_method}")(item)

    assert mocked_method.call_count == 2
