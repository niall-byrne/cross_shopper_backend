"""Test for the ReportsReadOnlyViewSet list view."""

from typing import TYPE_CHECKING, Any, Dict

import pytest
from api.views.reports.qs import qs_item, qs_scraper_config
from django.db.models import Prefetch, QuerySet
from reports.models import Report
from reports.models.serializers.report import ReportSerializer
from rest_framework import status

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet
  from rest_framework.test import APIClient
  from .conftest import AliasReportListUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportsReadOnlyViewSetList:

  def get_sorted_report_qs(self, filter: Dict[str, Any]) -> "QuerySet[Report]":
    return Report.objects.filter(**filter,).prefetch_related(
        Prefetch(
            "item",
            queryset=qs_item(),
        ),
    )

  def test_list__no_filter__returns_correct_response(
      self,
      client: "APIClient",
      report: "Report",
      report_list_url: "AliasReportListUrl",
  ) -> None:
    res = client.get(report_list_url())
    serializer = ReportSerializer(
        self.get_sorted_report_qs({"id": report.pk}),
        many=True,
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

  def test_list__filter_by_report_id__returns_correct_response(
      self,
      client: "APIClient",
      report: "Report",
      report_alternate: "Report",
      report_list_url: "AliasReportListUrl",
  ) -> None:
    res = client.get(report_list_url({"id": report_alternate.pk}))
    serializer = ReportSerializer(
        self.get_sorted_report_qs({"id": report_alternate.pk}),
        many=True,
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

  def test_list__filter_by_report_name__returns_correct_response(
      self,
      client: "APIClient",
      report: "Report",
      report_alternate: "Report",
      report_list_url: "AliasReportListUrl",
  ) -> None:
    res = client.get(report_list_url({"name": report_alternate.name}))
    serializer = ReportSerializer(
        self.get_sorted_report_qs({"id": report_alternate.pk}),
        many=True,
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

  def test_list__filter_by_uppercase_report_name__returns_correct_response(
      self,
      client: "APIClient",
      report: "Report",
      report_alternate: "Report",
      report_list_url: "AliasReportListUrl",
  ) -> None:
    res = client.get(report_list_url({"name": report_alternate.name.upper()}))
    serializer = ReportSerializer(
        self.get_sorted_report_qs({"id": report_alternate.pk}),
        many=True,
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

  @pytest.mark.parametrize("sc_active", (True, False))
  def test_list__filter_by_sc_active__vary_active__returns_correct_response(
      self,
      client: "APIClient",
      report: "Report",
      report_list_url: "AliasReportListUrl",
      sc_active: bool,
  ) -> None:
    res = client.get(report_list_url({"is_active": sc_active}))

    prefetched_scraper_config = qs_scraper_config().filter(is_active=sc_active)
    prefetched_item = qs_item().prefetch_related(
        Prefetch(
            "scraper_config",
            queryset=prefetched_scraper_config,
        )
    )
    filtered_reports = Report.objects.filter(id=report.pk).prefetch_related(
        Prefetch(
            "item",
            queryset=prefetched_item,
        )
    )

    serializer = ReportSerializer(
        filtered_reports,
        many=True,
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
