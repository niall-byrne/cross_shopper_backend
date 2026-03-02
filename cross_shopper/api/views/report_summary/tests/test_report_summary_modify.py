"""Test for the ReportReadOnlyViewSet modify view."""

from typing import TYPE_CHECKING

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from .conftest import AliasReportSummaryDetailUrl

if TYPE_CHECKING:  # no cover
  from reports.models import Report


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportReadOnlyViewSet:
  """Tests for the ReportReadOnlyViewSet modify view."""

  def test_modify__forbids_access(
      self,
      client: APIClient,
      report: "Report",
      report_summary_detail_url: AliasReportSummaryDetailUrl,
  ) -> None:
    res = client.put(report_summary_detail_url(report.pk), data={})

    assert res.status_code == status.HTTP_403_FORBIDDEN
