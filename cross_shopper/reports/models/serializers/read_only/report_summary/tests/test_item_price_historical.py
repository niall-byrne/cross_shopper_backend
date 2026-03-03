"""Tests for the ReportSummaryHistoricalItemPriceSerializerRO."""

from typing import Dict

import pytest
from reports.models import Report
from reports.models.serializers.read_only.report_summary.\
  item_price_historical import (
    ReportSummaryHistoricalItemPriceSerializerRO,
)


@pytest.mark.django_db
class TestReportSummaryHistoricalItemPriceSerializerRO:

  @pytest.mark.usefixtures(
      "report_summary_mocked_pricing_aggregate_last_52_weeks_manager"
  )
  def test_serialization__specified_item__returns_correct_representation(
      self,
      report_prefetched: Report,
      report_summary_mocked_pricing_aggregate_attributes: Dict[str, str],
  ) -> None:
    serializer = ReportSummaryHistoricalItemPriceSerializerRO(
        report_prefetched.item.all()[0],
        context={'report': report_prefetched},
    )

    data = serializer.data

    assert data == report_summary_mocked_pricing_aggregate_attributes

  def test_serialization__no_report_context__returns_none(
      self,
      report_prefetched: Report,
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

  def test_repr__specified_context__returns_correct_string(
      self,
      report: Report,
      report_context_2024: Dict,
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

  def test_get_average__multiple_instances__same_context__shares_cache(
      self,
      report_prefetched: Report,
      report_context_2024: Dict,
      report_summary_mocked_price_aggregate_average: pytest.fixture,
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

    res1 = serializer1.get_average(item)
    res2 = serializer2.get_average(item)

    assert res1 == res2
    assert report_summary_mocked_price_aggregate_average.call_count == 1

  def test_get_average__multiple_instances__different_context__isolated_cache(
      self,
      report_prefetched: Report,
      report_context_2024: Dict,
      report_context_2024_alternate: Dict,
      report_summary_mocked_price_aggregate_average: pytest.fixture,
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

    serializer1.get_average(item)
    serializer2.get_average(item)

    assert report_summary_mocked_price_aggregate_average.call_count == 2

  def test_serialization__no_prices__returns_none(
      self,
      report_prefetched: Report,
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
