"""Test for the PricingViewSet retrieve view."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from pricing.models.serializers.read_write.pricing import PricingSerializerRW
from rest_framework import status

if TYPE_CHECKING:
  from pricing.models import Price
  from rest_framework.test import APIClient
  from .conftest import AliasPricingDetailUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestPricingViewSetRetrieve:

  def test_retrieve__returns_correct_response(
      self,
      client: APIClient,
      price_today: Price,
      pricing_detail_url: AliasPricingDetailUrl,
  ) -> None:
    res = client.get(pricing_detail_url(price_today.pk))
    serializer = PricingSerializerRW(price_today)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
