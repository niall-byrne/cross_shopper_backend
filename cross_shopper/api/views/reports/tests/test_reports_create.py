"""Test for the ReportsPricingReadOnlyViewSet create view."""

from typing import TYPE_CHECKING

import pytest
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
class TestReportsViewSetCreate:
  """Tests for the ReportsPricingReadOnlyViewSet create view."""

  def test_create__forbids_access(
      self,
      client: APIClient,
      report: "Report",
      report_list_url: AliasReportListUrl,
  ) -> None:
    res = client.post(report_list_url(), data={})

    assert res.status_code == status.HTTP_403_FORBIDDEN
