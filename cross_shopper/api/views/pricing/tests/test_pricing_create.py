"""Test the PricingViewSet create view."""

from typing import TYPE_CHECKING

import pytest
from pricing.models.serializers.pricing import PricingSerializer
from rest_framework import status

if TYPE_CHECKING:  # no cover
  from pricing.models import Price
  from rest_framework.test import APIClient
  from .conftest import AliasPricingListUrl


@pytest.mark.django_db
class TestPricingViewSetCreateNoAuthentication:

  def test_create__forbids_access(
      self,
      unauthenticated_client: "APIClient",
      pricing_list_url: "AliasPricingListUrl",
      price_today: "Price",
  ) -> None:
    serializer = PricingSerializer(price_today)

    res = unauthenticated_client.post(pricing_list_url(), data=serializer.data)

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestPricingViewSetCreateAuthentication:

  def test_create__existing_object__returns_correct_response(
      self,
      authenticated_client: "APIClient",
      pricing_list_url: "AliasPricingListUrl",
      price_today: "Price",
  ) -> None:
    serializer = PricingSerializer(price_today)

    res = authenticated_client.post(pricing_list_url(), data=serializer.data)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

  def test_create__new_object__returns_correct_response(
      self,
      authenticated_client: "APIClient",
      pricing_list_url: "AliasPricingListUrl",
      price_today: "Price",
  ) -> None:
    serializer = PricingSerializer(price_today)
    data = serializer.data
    data.pop('id')
    price_today.delete()

    res = authenticated_client.post(pricing_list_url(), data=data)
    received_data_without_id = dict(res.data)
    received_data_without_id.pop('id')

    assert res.status_code == status.HTTP_201_CREATED
    assert received_data_without_id == data
