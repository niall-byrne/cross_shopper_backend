"""Test for the ReportTargetReadOnlyViewSet list view."""

from typing import TYPE_CHECKING, Any, Dict

import pytest
from django.db.models import QuerySet
from reports.models import Report
from reports.models.serializers.read_only.report_target import (
    ReportTargetSerializerRO,
)
from rest_framework import status

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet
  from reports.models import Report
  from rest_framework.test import APIClient
  from .conftest import AliasReportTargetListUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportTargetReadOnlyViewSetList:

  def get_sorted_report_qs(self, filter: Dict[str, Any]) -> "QuerySet[Report]":
    return Report.objects.filter(**filter)

  @pytest.mark.usefixtures("report", "report_testing")
  def test_list__no_filter__returns_correct_response(
      self,
      client: "APIClient",
      report: "Report",
      report_target_list_url: "AliasReportTargetListUrl",
  ) -> None:
    serializer = ReportTargetSerializerRO(
        self.get_sorted_report_qs({}),
        many=True,
    )

    res = client.get(report_target_list_url())

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

  @pytest.mark.usefixtures("report")
  def test_list__filter_by_report_id__returns_correct_response(
      self,
      client: "APIClient",
      report_alternate: "Report",
      report_target_list_url: "AliasReportTargetListUrl",
  ) -> None:
    serializer = ReportTargetSerializerRO(
        self.get_sorted_report_qs({"id": report_alternate.pk}),
        many=True,
    )

    res = client.get(report_target_list_url({"id": report_alternate.pk}))

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

  @pytest.mark.usefixtures("report")
  def test_list__filter_by_report_name__returns_correct_response(
      self,
      client: "APIClient",
      report_alternate: "Report",
      report_target_list_url: "AliasReportTargetListUrl",
  ) -> None:
    serializer = ReportTargetSerializerRO(
        self.get_sorted_report_qs({"id": report_alternate.pk}),
        many=True,
    )

    res = client.get(report_target_list_url({"name": report_alternate.name}))

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

  def test_list__filter_by_uppercase_report_name__returns_correct_response(
      self,
      client: "APIClient",
      report: "Report",
      report_alternate: "Report",
      report_target_list_url: "AliasReportTargetListUrl",
  ) -> None:
    res = client.get(
        report_target_list_url({"name": report_alternate.name.upper()})
    )
    serializer = ReportTargetSerializerRO(
        self.get_sorted_report_qs({"id": report_alternate.pk}),
        many=True,
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

  @pytest.mark.usefixtures("report", "report_testing")
  @pytest.mark.parametrize("is_testing", (True, False))
  def test_list__filter_by_testing__is_testing__returns_correct_response(
      self,
      client: "APIClient",
      report_target_list_url: "AliasReportTargetListUrl",
      is_testing: bool,
  ) -> None:
    serializer = ReportTargetSerializerRO(
        self.get_sorted_report_qs({"is_testing": is_testing}),
        many=True,
    )

    res = client.get(report_target_list_url({"is_testing": is_testing}))

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
