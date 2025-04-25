"""Test for the ReportsPricingReadOnlyViewSet list view."""

from typing import TYPE_CHECKING, cast

import pytest
from django.conf import settings
from reports.models.serializers.report import ReportSerializer
from rest_framework import status
from rest_framework.test import APIClient
from .conftest import AliasReportListUrl

if TYPE_CHECKING:  # no cover
  from reports.models import Report


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportsViewSetList:
  """Tests for the ReportsPricingReadOnlyViewSet list view."""

  def test_list__no_filter__returns_correct_response(
      self,
      client: APIClient,
      report: "Report",
      report_list_url: AliasReportListUrl,
  ) -> None:
    res = client.get(report_list_url())
    serializer = ReportSerializer(report)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == [serializer.data]

  def test_list__filter_by_report_id__returns_correct_response(
      self,
      client: APIClient,
      report: "Report",
      report_alternate: "Report",
      report_list_url: AliasReportListUrl,
  ) -> None:
    res = client.get(report_list_url({"id": report_alternate.id}))
    serializer = ReportSerializer(report_alternate)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == [serializer.data]

  def test_list__filter_by_report_name__returns_correct_response(
      self,
      client: APIClient,
      report: "Report",
      report_alternate: "Report",
      report_list_url: AliasReportListUrl,
  ) -> None:
    res = client.get(report_list_url({"name": report_alternate.name}))
    serializer = ReportSerializer(report_alternate)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == [serializer.data]

  def test_list__filter_by_uppercase_report_name__returns_correct_response(
      self,
      client: APIClient,
      report: "Report",
      report_alternate: "Report",
      report_list_url: AliasReportListUrl,
  ) -> None:
    res = client.get(report_list_url({"name": report_alternate.name.upper()}))
    serializer = ReportSerializer(report_alternate)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == [serializer.data]

  def test_list__filter_by_testing__testing_only__returns_correct_response(
      self,
      client: APIClient,
      report: "Report",
      report_testing: "Report",
      report_list_url: AliasReportListUrl,
  ) -> None:
    query_param = cast(
        str,
        getattr(
            settings,
            "QUERY_PARAMETER_REPORT_TESTING",
            None,
        ),
    )
    res = client.get(report_list_url({query_param: 1}))
    serializer = ReportSerializer(report_testing)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == [serializer.data]

  def test_list__filter_by_testing__non_testing_only__returns_correct_response(
      self,
      client: APIClient,
      report: "Report",
      report_testing: "Report",
      report_list_url: AliasReportListUrl,
  ) -> None:
    res = client.get(report_list_url())
    serializer = ReportSerializer(report)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == [serializer.data]
