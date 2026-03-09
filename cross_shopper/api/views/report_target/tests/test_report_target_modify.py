"""Test for the ReportTargetReadOnlyViewSet modify view."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from rest_framework import status

if TYPE_CHECKING:
  from reports.models import Report
  from rest_framework.test import APIClient
  from .conftest import AliasTargetReportDetailUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportTargetReadOnlyViewSetModify:

  def test_modify__forbids_access(
      self,
      client: APIClient,
      report: Report,
      report_target_detail_url: AliasTargetReportDetailUrl,
  ) -> None:
    res = client.put(report_target_detail_url(report.pk), data={})

    assert res.status_code == status.HTTP_403_FORBIDDEN
