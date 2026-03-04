"""Tests for the ReportSummarySerializer."""

from typing import TYPE_CHECKING

import pytest
from freezegun import freeze_time
from reports.models.serializers.report_summary.item import (
    ReportSummaryItemSerializer,
)
from reports.models.serializers.report_summary.report import (
    ReportSummarySerializer,
)
from reports.models.serializers.report_summary.store import (
    ReportSummaryStoreSerializer,
)

if TYPE_CHECKING:  # no cover
  from reports.models.report import Report


@pytest.mark.django_db
class TestReportSummarySerializer:

  @freeze_time("2024-01-01 12:00:00")
  @pytest.mark.parametrize(
      "week,year,timestamp", (("1", "2024", "Mon, 01 Jan 2024 12:00:00 GMT"),)
  )
  def test_serialization__specified_report__returns_correct_representation(
      self,
      report_prefetched: "Report",
      timestamp: str,
      week: str,
      year: str,
  ) -> None:
    serializer = ReportSummarySerializer(
        report_prefetched,
        context={
            "week": week,
            "year": year
        },
    )

    assert serializer.data == {
        "id":
            report_prefetched.pk,
        "name":
            report_prefetched.name,
        "week":
            week,
        "year":
            year,
        "generated_at":
            timestamp,
        "store":
            ReportSummaryStoreSerializer(
                report_prefetched.store.all(),
                many=True,
            ).data,
        "item":
            ReportSummaryItemSerializer(
                report_prefetched.item.all(),
                many=True,
                context={
                    **serializer.context,
                    "report": report_prefetched,
                },
            ).data
    }
