"""Tests for the ReportSummaryViewSet."""

import decimal
from typing import Any

import pytest
from items.models import Item
from pricing.models import Price
from pricing.models.defaults.default_pricing_week import default_pricing_week
from pricing.models.defaults.default_pricing_year import default_pricing_year
from pricing.models.factories.pricing import PriceFactory
from reports.models import Report
from reports.models.serializers.report_summary.report import (
    ReportSummarySerializer,
)
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportSummaryViewSet:
  """Tests for the ReportSummaryViewSet."""

  def test_list__all_reports__returns_correct_representation(
      self,
      client: APIClient,
      report: Report,
      report_summary_list_url: Any,
  ) -> None:
    res = client.get(report_summary_list_url())
    serializer = ReportSummarySerializer(report)

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1
    assert res.data[0] == serializer.data

  def test_list__filter_by_id__returns_one_report(
      self,
      client: APIClient,
      report: Report,
      report_summary_list_url: Any,
  ) -> None:
    res = client.get(report_summary_list_url({'id': report.id}))

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1

  def test_retrieve__specified_report__returns_correct_report_data(
      self,
      client: APIClient,
      report_prefetched: Report,
      report_summary_detail_url: Any,
  ) -> None:
    res = client.get(report_summary_detail_url(report_prefetched.id))
    serializer = ReportSummarySerializer(
        report_prefetched,
        context={
            'week': default_pricing_week(),
            'year': default_pricing_year(),
        },
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data['id'] == report_prefetched.id
    assert res.data['name'] == report_prefetched.name
    assert res.data['week'] == serializer.data['week']
    assert res.data['year'] == serializer.data['year']
    assert res.data['generated_at'] == serializer.data['generated_at']

  def test_retrieve__specified_report__returns_correct_store_data(
      self,
      client: APIClient,
      report_prefetched: Report,
      report_summary_detail_url: Any,
  ) -> None:
    res = client.get(report_summary_detail_url(report_prefetched.id))
    serializer = ReportSummarySerializer(
        report_prefetched,
        context={
            'week': default_pricing_week(),
            'year': default_pricing_year(),
        },
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data['store'] == serializer.data['store']

  def test_retrieve__specified_report__returns_correct_item_data(
      self,
      client: APIClient,
      report_prefetched: Report,
      report_summary_detail_url: Any,
  ) -> None:
    res = client.get(report_summary_detail_url(report_prefetched.id))
    serializer = ReportSummarySerializer(
        report_prefetched,
        context={
            'week': default_pricing_week(),
            'year': default_pricing_year(),
        },
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data['item'] == serializer.data['item']

  def test_retrieve__default_week_and_year__returns_none_for_missing_prices(
      self,
      client: APIClient,
      report_with_item: Report,
      report_summary_detail_url: Any,
      item: Item,
  ) -> None:
    store = list(report_with_item.store.all())[0]
    Price.objects.create(
        item=item,
        store=store,
        amount=decimal.Decimal('99.99'),
        year=2025,
        week=10,
    )

    res = client.get(report_summary_detail_url(report_with_item.id))
    per_store = res.data['item'][0]['price']['selected_week']['per_store']

    assert per_store == {str(store.id): None}

  def test_retrieve__specified_week_and_year__returns_correct_prices(
      self,
      client: APIClient,
      report_with_item: Report,
      report_summary_detail_url: Any,
      item: Item,
  ) -> None:
    store = list(report_with_item.store.all())[0]
    Price.objects.create(
        item=item,
        store=store,
        amount=decimal.Decimal('99.99'),
        year=2025,
        week=10,
    )

    res = client.get(
        report_summary_detail_url(report_with_item.id), {
            'week': 10,
            'year': 2025
        }
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data['item'][0]['price']['selected_week']['per_store'] == {
        str(store.id): '99.99'
    }
