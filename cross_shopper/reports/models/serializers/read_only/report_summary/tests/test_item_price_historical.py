"""Tests for the ReportSummaryHistoricalItemPriceSerializerRO."""

from typing import TYPE_CHECKING

import pytest
from reports.models import Report
from reports.models.serializers.read_only.report_summary.\
  item_price_historical import (
    ReportSummaryHistoricalItemPriceSerializerRO,
)

if TYPE_CHECKING:  # no cover
  from typing import Dict


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

    assert serializer.data == report_summary_mocked_pricing_aggregate_attributes

  def test_serialization__no_report_context__returns_none(
      self,
      report_prefetched: "Report",
  ) -> None:
    serializer = ReportSummaryHistoricalItemPriceSerializerRO(
        report_prefetched.item.all()[0],
        context={},
    )

    assert serializer.data == {
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

    assert serializer.data == {
        'average': None,
        'high': None,
        'low': None,
    }
