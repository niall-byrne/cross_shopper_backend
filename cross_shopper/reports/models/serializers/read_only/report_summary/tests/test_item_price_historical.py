"""Tests for the ReportSummaryHistoricalItemPriceSerializerRO."""

from typing import TYPE_CHECKING, Dict

import pytest
from reports.models.serializers.read_only.report_summary.\
  item_price_historical import (
    ReportSummaryHistoricalItemPriceSerializerRO,
)

if TYPE_CHECKING:  # no cover
  from typing import Any, Dict

  from reports.models import Report
  from .conftest import AliasSerializerMockCreator


@pytest.mark.django_db
class TestReportSummaryHistoricalItemPriceSerializerRO:

  @pytest.mark.usefixtures(
      "report_summary_mocked_pricing_aggregate_last_52_weeks_manager"
  )
  def test_serialization__specified_item__returns_correct_representation(
      self,
      report_prefetched: "Report",
      report_summary_mocked_pricing_aggregate_attributes: "Dict[str, str]",
  ) -> None:
    serializer = ReportSummaryHistoricalItemPriceSerializerRO(
        report_prefetched.item.all()[0],
        context={'report': report_prefetched},
    )

    data = serializer.data

    assert data == report_summary_mocked_pricing_aggregate_attributes

  def test_serialization__no_report_context__returns_none(
      self,
      report_prefetched: "Report",
  ) -> None:
    serializer = ReportSummaryHistoricalItemPriceSerializerRO(
        report_prefetched.item.all()[0],
        context={},
    )

    data = serializer.data

    assert data == {
        'average': None,
        'high': None,
        'low': None,
    }

  def test_serialization__no_prices__returns_none(
      self,
      report_prefetched: "Report",
  ) -> None:
    serializer = ReportSummaryHistoricalItemPriceSerializerRO(
        report_prefetched.item.all()[0],
        context={'report': report_prefetched},
    )

    data = serializer.data

    assert data == {
        'average': None,
        'high': None,
        'low': None,
    }

  def test_repr__specified_context__returns_correct_string(
      self,
      report: "Report",
      report_context_2024: "Dict[str, Any]",
  ) -> None:
    serializer = ReportSummaryHistoricalItemPriceSerializerRO(
        report.item.all()[0],
        context=report_context_2024,
    )

    serializer_repr = repr(serializer)

    assert serializer_repr == ":".join(
        [
            repr(report_context_2024['week']),
            repr(report_context_2024['year']),
            repr(report_context_2024['report']),
            repr(ReportSummaryHistoricalItemPriceSerializerRO),
        ]
    )

  @pytest.mark.parametrize("cached_method", (
      "average",
      "high",
      "low",
  ))
  def test_cached_method__multiple_instances__same_context__shares_cache(
      self,
      report_prefetched: "Report",
      report_context_2024: "Dict[str, Any]",
      create_mocked_price_aggregate_manager: "AliasSerializerMockCreator",
      cached_method: "str",
  ) -> None:
    item = report_prefetched.item.all()[0]
    serializer1 = ReportSummaryHistoricalItemPriceSerializerRO(
        item,
        context=report_context_2024,
    )
    serializer2 = ReportSummaryHistoricalItemPriceSerializerRO(
        item,
        context=report_context_2024,
    )
    mocked_method = create_mocked_price_aggregate_manager(cached_method)

    res1 = getattr(serializer1, f"get_{cached_method}")(item)
    res2 = getattr(serializer2, f"get_{cached_method}")(item)

    assert res1 == res2
    assert mocked_method.call_count == 1

  @pytest.mark.parametrize("cached_method", (
      "average",
      "high",
      "low",
  ))
  def test_cached_method__multiple_instances__different_context__isolated_cache(
      self,
      report_prefetched: "Report",
      report_context_2024: "Dict[str, Any]",
      report_context_2024_alternate: "Dict[str, Any]",
      create_mocked_price_aggregate_manager: "AliasSerializerMockCreator",
      cached_method: "str",
  ) -> None:
    item = report_prefetched.item.all()[0]
    serializer1 = ReportSummaryHistoricalItemPriceSerializerRO(
        item,
        context=report_context_2024,
    )
    serializer2 = ReportSummaryHistoricalItemPriceSerializerRO(
        item,
        context=report_context_2024_alternate,
    )
    mocked_method = create_mocked_price_aggregate_manager(cached_method)

    getattr(serializer1, f"get_{cached_method}")(item)
    getattr(serializer2, f"get_{cached_method}")(item)

    assert mocked_method.call_count == 2
