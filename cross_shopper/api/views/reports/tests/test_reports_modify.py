"""Test for the ReportsPricingReadOnlyViewSet modify view."""

from typing import TYPE_CHECKING

import pytest
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
class TestReportsViewSetModify:
  """Tests for the ReportsPricingReadOnlyViewSet modify view."""

  def test_modify__forbids_access(
      self,
      client: APIClient,
      report: "Report",
      report_detail_url: AliasReportDetailUrl,
  ) -> None:
    res = client.put(report_detail_url(report.id), data={})

    assert res.status_code == status.HTTP_403_FORBIDDEN
