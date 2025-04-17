"""Test for the PricingViewSet retrieve view."""

from typing import TYPE_CHECKING

import pytest
from pricing.models.serializers.pricing import PricingSerializer
from rest_framework import status
from rest_framework.test import APIClient
from .conftest import AliasPricingDetailUrl

if TYPE_CHECKING:  # no cover
  from pricing.models import Price


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestPricingViewSetRetrieve:
  """Tests for the PricingViewSet retrieve view."""

  def test_retrieve__returns_correct_response(
      self,
      client: APIClient,
      price_today: "Price",
      pricing_detail_url: AliasPricingDetailUrl,
  ) -> None:
    res = client.get(pricing_detail_url(price_today.id))
    serializer = PricingSerializer(price_today)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
