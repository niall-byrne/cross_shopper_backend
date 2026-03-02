"""Test for the ReportsReadOnlyViewSet retrieve view."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
from api.views.reports.qs import qs_item
from django.db.models import Prefetch
from reports.models import Report
from reports.models.serializers.read_only.report import ReportSerializerRO
from rest_framework import status

if TYPE_CHECKING:
  from django.db.models import QuerySet
  from rest_framework.test import APIClient
  from .conftest import AliasReportDetailUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportsReadOnlyViewSetRetrieve:

  def get_sorted_report_qs(self, filter: dict[str, Any]) -> QuerySet[Report]:
    return Report.objects.filter(**filter,).prefetch_related(
        Prefetch(
            "item",
            queryset=qs_item(),
        ),
    )

  def test_retrieve__returns_correct_response(
      self,
      client: APIClient,
      report: Report,
      report_detail_url: AliasReportDetailUrl,
  ) -> None:
    res = client.get(report_detail_url(report.pk))
    serializer = ReportSerializerRO(
        self.get_sorted_report_qs({
            "id": report.pk
        }).first()
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
