"""Test for the ReportsPricingReadOnlyViewSet retrieve view."""

from typing import TYPE_CHECKING

import pytest
from reports.models.serializers.report import ReportSerializer
from rest_framework import status
from rest_framework.test import APIClient
from .conftest import AliasReportDetailUrl

if TYPE_CHECKING:  # no cover
  from reports.models import Report


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportsViewSetRetrieve:
  """Tests for the ReportsPricingReadOnlyViewSet retrieve view."""

  def test_retrieve__returns_correct_response(
      self,
      client: APIClient,
      report: "Report",
      report_detail_url: AliasReportDetailUrl,
  ) -> None:
    res = client.get(report_detail_url(report.id))
    serializer = ReportSerializer(report)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
