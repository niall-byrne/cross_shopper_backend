"""Test for the ReportsReadOnlyViewSet modify view."""

from typing import TYPE_CHECKING

import pytest
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
class TestReportsReadOnlyViewSetModify:

  def test_modify__forbids_access(
      self,
      client: "APIClient",
      report: "Report",
      report_detail_url: "AliasReportDetailUrl",
  ) -> None:
    res = client.put(report_detail_url(report.pk), data={})

    assert res.status_code == status.HTTP_403_FORBIDDEN
