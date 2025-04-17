"""Test for the ReportsReadOnlyViewSet create view."""

from typing import TYPE_CHECKING

import pytest
from rest_framework import status

if TYPE_CHECKING:  # no cover
  from rest_framework.test import APIClient
  from .conftest import AliasReportListUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportsReadOnlyViewSetCreate:

  def test_create__forbids_access(
      self,
      client: "APIClient",
      report_list_url: "AliasReportListUrl",
  ) -> None:
    res = client.post(report_list_url(), data={})

    assert res.status_code == status.HTTP_403_FORBIDDEN
