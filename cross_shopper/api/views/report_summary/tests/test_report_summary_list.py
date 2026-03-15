"""Tests for the ReportSummaryReadOnlyViewSet list view."""

from typing import TYPE_CHECKING, Any, Dict

import pytest
from pricing.models.defaults.default_pricing_week import default_pricing_week
from pricing.models.defaults.default_pricing_year import default_pricing_year
from reports.models.serializers.read_only.report_summary import (
    ReportSummarySerializerRO,
)
from reports.models.serializers.read_only.report_summary.item import (
    ReportSummaryItemSerializerRO,
)
from rest_framework import status

if TYPE_CHECKING:  # no cover
  from pricing.models.fixtures.pricing import (
    AliasCreateLast52PriceBatchFromReport,
  )
  from reports.models.report import Report
  from rest_framework.test import APIClient
  from .conftest import AliasReportSummaryListUrl


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
    serializer = ReportSummarySerializerRO(
        target_report,
        context={
            'week': str(default_pricing_week()),
            'year': str(default_pricing_year()),
        },
    )
    return serializer.data

  def remove_report_summary_timestamp(
      self,
      report_data: "Dict[str, Any]",
  ) -> "Dict[str, Any]":
    report_data.pop("generated_at")
    return report_data

  @pytest.mark.usefixtures("report_prefetched", "report_prefetched_alternate")
  def test_list__all_reports__returns_200_with_two_reports(
      self,
      client: "APIClient",
      report_summary_list_url: "AliasReportSummaryListUrl",
  ) -> None:

    res = client.get(report_summary_list_url())

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 2

  def test_list__all_reports__returns_correct_representation(
      self,
      client: "APIClient",
      report_prefetched: "Report",
      report_prefetched_alternate: "Report",
      report_summary_list_url: "AliasReportSummaryListUrl",
  ) -> None:
    expected1 = self.get_serialized_report_summary(report_prefetched)
    expected2 = self.get_serialized_report_summary(report_prefetched_alternate)
    self.remove_report_summary_timestamp(expected1)
    self.remove_report_summary_timestamp(expected2)

    res = client.get(report_summary_list_url())

    response = list(map(self.remove_report_summary_timestamp, res.data))
    assert response == [expected1, expected2]

  @pytest.mark.usefixtures("report_prefetched_alternate")
  def test_list__filter_by_id__returns_correct_report(
      self,
      client: "APIClient",
      report_prefetched: "Report",
      report_summary_list_url: "AliasReportSummaryListUrl",
  ) -> None:
    res = client.get(report_summary_list_url({'id': report_prefetched.pk}))

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1
    assert res.data[0]['id'] == report_prefetched.pk

  @pytest.mark.usefixtures("report_prefetched_alternate")
  def test_list__filter_by_name__returns_correct_report(
      self,
      client: "APIClient",
      report_prefetched: "Report",
      report_summary_list_url: "AliasReportSummaryListUrl",
  ) -> None:
    res = client.get(report_summary_list_url({'name': report_prefetched.name}))

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1
    assert res.data[0]['name'] == report_prefetched.name

  @pytest.mark.usefixtures("report_prefetched_alternate")
  def test_list__filter_by_is_testing__returns_correct_report(
      self,
      client: "APIClient",
      report_prefetched_testing: "Report",
      report_summary_list_url: "AliasReportSummaryListUrl",
  ) -> None:
    res = client.get(report_summary_list_url({'is_testing': True}))

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1
    assert res.data[0]['id'] == report_prefetched_testing.pk

  def test_retrieve__specified_year_week__filters_price_data_correctly(
      self,
      client: "APIClient",
      create_last_52_price_batch_from_report:
      "AliasCreateLast52PriceBatchFromReport",
      report_prefetched: "Report",
      report_prefetched_alternate: "Report",
      report_summary_list_url: "AliasReportSummaryListUrl",
  ) -> None:
    week = "3"
    year = str(default_pricing_year() - 1)
    create_last_52_price_batch_from_report(report_prefetched)

    res = client.get(
        report_summary_list_url(),
        data={
            "week": week,
            'year': year
        },
    )

    for response, report in zip(
        res.data, [report_prefetched, report_prefetched_alternate]
    ):
      assert response['item'] == ReportSummaryItemSerializerRO(
          report.item.all(),
          many=True,
          context={
              'report': report,
              'week': week,
              'year': year,
          }
      ).data
