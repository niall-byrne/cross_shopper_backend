"""Tests for the PricingViewSet list view."""

from typing import TYPE_CHECKING, cast

import pytest
from pricing.models import Price
from pricing.models.factories.pricing import PriceFactory
from pricing.models.serializers.read_write.pricing import PricingSerializerRW
from rest_framework import status

if TYPE_CHECKING:  # no cover
  from items.models import Item
  from reports.models import Report
  from rest_framework.test import APIClient
  from stores.models import Store
  from .conftest import AliasPricingListUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestPricingViewSetList:
  """Tests for the PricingViewSet list view."""

  def test_list__no_filter__returns_correct_response(
      self,
      client: "APIClient",
      pricing_list_url: "AliasPricingListUrl",
      report_with_pricing: "Report",
  ) -> None:
    all_items = report_with_pricing.item.all()
    all_stores = report_with_pricing.store.all()
    query = Price.objects.filter(
        item__in=all_items,
        store__in=all_stores,
    )
    serializer = PricingSerializerRW(query, many=True)

    res = client.get(pricing_list_url())

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

  def test_list__filter_by_item_id__returns_correct_response(
      self,
      client: "APIClient",
      pricing_list_url: "AliasPricingListUrl",
      report_with_pricing: "Report",
  ) -> None:
    first_item = cast("Item", report_with_pricing.item.first())
    all_stores = report_with_pricing.store.all()
    query = Price.objects.filter(
        item=first_item.pk,
        store__in=all_stores,
    )

    res = client.get(pricing_list_url({"itemId": first_item.pk}))
    serializer = PricingSerializerRW(query, many=True)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

  def test_list__filter_by_store_id__returns_correct_response(
      self,
      client: "APIClient",
      pricing_list_url: "AliasPricingListUrl",
      report_with_pricing: "Report",
  ) -> None:
    all_items = report_with_pricing.item.all()
    last_store = cast("Store", report_with_pricing.store.last())
    query = Price.objects.filter(
        item__in=all_items,
        store=last_store.pk,
    )

    res = client.get(pricing_list_url({"storeId": last_store.pk}))
    serializer = PricingSerializerRW(query, many=True)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

  def test_list__filter_by_date__returns_correct_response(
      self,
      client: "APIClient",
      pricing_list_url: "AliasPricingListUrl",
      report_with_pricing: "Report",
  ) -> None:
    all_items = report_with_pricing.item.all()
    all_stores = report_with_pricing.store.all()
    price = PriceFactory.create(
        item=all_items.first(),
        store=all_stores.first(),
        week=1,
        year=2024,
    )

    res = client.get(pricing_list_url({"week": 1, "year": 2024}))
    serializer = PricingSerializerRW(price)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == [serializer.data]
