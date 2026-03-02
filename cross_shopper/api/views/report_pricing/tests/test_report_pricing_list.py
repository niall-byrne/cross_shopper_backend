"""Test the ReportPricingReadOnlyViewSet list view."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from reports.models.serializers.read_only.report_pricing import (
    ReportPricingSerializerRO,
)
from rest_framework import status

if TYPE_CHECKING:
  from reports.models import Report
  from rest_framework.test import APIClient
  from .conftest import AliasReportPricingListUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportPricingReadOnlyViewSetList:

  def test_list__returns_correct_response(
      self,
      client: APIClient,
      report_pricing_list_url: AliasReportPricingListUrl,
      report_with_pricing: Report,
  ) -> None:
    serializer = ReportPricingSerializerRO(
        report_with_pricing.item,
        context={"report": report_with_pricing},
        many=True,
    )

    res = client.get(report_pricing_list_url(report_with_pricing.pk))

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
