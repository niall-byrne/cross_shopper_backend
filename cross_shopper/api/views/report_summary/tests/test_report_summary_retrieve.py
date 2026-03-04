"""Tests for the ReportSummaryReadOnlyViewSet retrieve view."""

from typing import TYPE_CHECKING

import pytest
from pricing.models.defaults.default_pricing_week import default_pricing_week
from pricing.models.defaults.default_pricing_year import default_pricing_year
from reports.models.report import Report
from reports.models.serializers.report_summary.item import (
    ReportSummaryItemSerializer,
)
from reports.models.serializers.report_summary.report import (
    ReportSummarySerializer,
)
from rest_framework import status
from rest_framework.test import APIClient

if TYPE_CHECKING:
  from typing import Any, Dict

  from pricing.models.fixtures.pricing import (
      AliasCreateLast52PriceBatchFromReport,
  )
  from .conftest import AliasReportSummaryDetailUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportSummaryReadOnlyViewSet:

  def get_serialized_report_summary(
      self,
      target_report: "Report",
  ) -> "Dict[str, Any]":
    serializer = ReportSummarySerializer(
        target_report,
        context={
            "week": str(default_pricing_week()),
            "year": str(default_pricing_year()),
        },
    )
    return serializer.data

  def remove_report_summary_timestamp(
      self,
      report_data: "Dict[str, Any]",
  ) -> "Dict[str, Any]":
    report_data.pop("generated_at")
    return report_data

  @pytest.mark.usefixtures("report_prefetched_alternate")
  def test_retrieve__200_with_correct_report(
      self,
      client: APIClient,
      report_prefetched: "Report",
      report_summary_detail_url: "AliasReportSummaryDetailUrl",
  ) -> None:
    expected1 = self.get_serialized_report_summary(report_prefetched)

    res = client.get(report_summary_detail_url(report_prefetched.pk))

    assert res.status_code == status.HTTP_200_OK
    assert res.data["id"] == expected1["id"]

  @pytest.mark.usefixtures("report_prefetched_alternate")
  def test_retrieve__has_correct_representation(
      self,
      client: "APIClient",
      report_prefetched: "Report",
      report_summary_detail_url: "AliasReportSummaryDetailUrl",
  ) -> None:
    expected1 = self.get_serialized_report_summary(report_prefetched)
    self.remove_report_summary_timestamp(expected1)

    res = client.get(report_summary_detail_url(report_prefetched.pk))

    response = self.remove_report_summary_timestamp(res.data)
    assert expected1 == response

  @pytest.mark.usefixtures("report_prefetched_alternate")
  def test_retrieve__specified_year_week__filters_price_data_correctly(
      self,
      client: "APIClient",
      create_last_52_price_batch_from_report:
      "AliasCreateLast52PriceBatchFromReport",
      report_prefetched: "Report",
      report_summary_detail_url: "AliasReportSummaryDetailUrl",
  ) -> None:
    week = "3"
    year = str(default_pricing_year() - 1)
    create_last_52_price_batch_from_report(report_prefetched)

    res = client.get(
        report_summary_detail_url(report_prefetched.pk),
        data={
            "week": week,
            "year": year
        },
    )

    assert (
        res.data["item"] == ReportSummaryItemSerializer(
            report_prefetched.item.all(),
            many=True,
            context={
                "report": report_prefetched,
                "week": week,
                "year": year,
            },
        ).data
    )
