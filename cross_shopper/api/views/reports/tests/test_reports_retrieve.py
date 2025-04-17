"""Test for the ReportsReadOnlyViewSet retrieve view."""

from typing import TYPE_CHECKING

import pytest
from reports.models.serializers.report import ReportSerializer
from rest_framework import status

if TYPE_CHECKING:  # no cover
  from reports.models import Report
  from rest_framework.test import APIClient
  from .conftest import AliasReportDetailUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportsReadOnlyViewSetRetrieve:
  """Tests for the ReportsReadOnlyViewSet retrieve view."""

  def test_retrieve__returns_correct_response(
      self,
      client: "APIClient",
      report: "Report",
      report_detail_url: "AliasReportDetailUrl",
  ) -> None:
    res = client.get(report_detail_url(report.pk))
    serializer = ReportSerializer(report)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
