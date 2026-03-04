"""Test for the ReportSummaryReadOnlyViewSet create view."""

from typing import TYPE_CHECKING

import pytest
from rest_framework import status

if TYPE_CHECKING:  # no cover
  from rest_framework.test import APIClient
  from .conftest import AliasReportSummaryListUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportSummaryReadOnlyViewSet:

  def test_create__forbids_access(
      self,
      client: "APIClient",
      report_summary_list_url: "AliasReportSummaryListUrl",
  ) -> None:
    res = client.post(report_summary_list_url(), data={})

    assert res.status_code == status.HTTP_403_FORBIDDEN
