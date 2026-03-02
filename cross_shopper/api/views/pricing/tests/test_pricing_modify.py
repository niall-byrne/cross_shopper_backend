"""Test the PricingViewSet modify view."""

from typing import TYPE_CHECKING

import pytest
from pricing.models.serializers.read_write.pricing import PricingSerializerRW
from rest_framework import status

if TYPE_CHECKING:  # no cover
  from pricing.models import Price
  from rest_framework.test import APIClient
  from .conftest import AliasPricingDetailUrl


@pytest.mark.django_db
class TestPricingViewSetModifyNoAuthentication:
  """Test the PricingViewSet modify view without authentication."""

  def test_put__forbids_access(
      self,
      unauthenticated_client: "APIClient",
      pricing_detail_url: "AliasPricingDetailUrl",
      price_today: "Price",
  ) -> None:
    serializer = PricingSerializerRW(price_today)

    res = unauthenticated_client.put(
        pricing_detail_url(price_today.pk),
        data=serializer.data,
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestPricingViewSetModifyAuthentication:
  """Test the PricingViewSet modify view with authentication."""

  def test_put__returns_correct_response(
      self,
      authenticated_client: "APIClient",
      pricing_detail_url: "AliasPricingDetailUrl",
      price_today: "Price",
  ) -> None:
    serializer = PricingSerializerRW(price_today)

    res = authenticated_client.put(
        pricing_detail_url(price_today.pk),
        data=serializer.data,
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
