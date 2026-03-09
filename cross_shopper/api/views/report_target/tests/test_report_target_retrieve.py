"""Test for the ReportTargetReadOnlyViewSet retrieve view."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from reports.models import Report
from reports.models.serializers.read_only.report_target import (
    ReportTargetSerializerRO,
)
from rest_framework import status

if TYPE_CHECKING:
  from rest_framework.test import APIClient
  from .conftest import AliasTargetReportDetailUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportTargetReadOnlyViewSetRetrieve:

  def test_retrieve__returns_correct_response(
      self,
      client: APIClient,
      report: Report,
      report_target_detail_url: AliasTargetReportDetailUrl,
  ) -> None:
    res = client.get(report_target_detail_url(report.pk))
    serializer = ReportTargetSerializerRO(Report.objects.get(pk=report.pk))

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
