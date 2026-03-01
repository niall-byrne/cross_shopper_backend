"""Tests for the ReportSummaryViewSet."""

import decimal
from typing import TYPE_CHECKING, Any, Optional

import pytest
from freezegun import freeze_time
from pricing.models.defaults.default_pricing_week import default_pricing_week
from pricing.models.defaults.default_pricing_year import default_pricing_year
from reports.models.report import Report
from reports.models.serializers.report_summary.report import (
    ReportSummarySerializer,
)
from rest_framework import status
from rest_framework.test import APIClient

if TYPE_CHECKING:
  from items.models import Item
  from pricing.models import Price


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
      report_prefetched: "Report",
      report_summary_list_url: Any,
  ) -> None:
    serializer = ReportSummarySerializer(
        report_prefetched,
        context={
            'week': str(default_pricing_week()),
            'year': str(default_pricing_year()),
        },
    )

    res = client.get(report_summary_list_url())

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1
    assert res.data[0] == serializer.data

  def test_list__filter_by_id__returns_one_report(
      self,
      client: APIClient,
      report: "Report",
      report_summary_list_url: Any,
  ) -> None:
    res = client.get(report_summary_list_url({'id': report.id}))

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1

  @freeze_time("2026-03-01 20:00:00")
  def test_retrieve__specified_report__returns_correct_report_data(
      self,
      client: APIClient,
      report_prefetched: "Report",
      report_summary_detail_url: Any,
  ) -> None:
    serializer = ReportSummarySerializer(
        report_prefetched,
        context={
            'week': str(default_pricing_week()),
            'year': str(default_pricing_year()),
        },
    )

    res = client.get(report_summary_detail_url(report_prefetched.id))

    assert res.status_code == status.HTTP_200_OK
    assert res.data['id'] == report_prefetched.id
    assert res.data['name'] == report_prefetched.name
    assert str(res.data['week']) == str(serializer.data['week'])
    assert str(res.data['year']) == str(serializer.data['year'])
    assert res.data['generated_at'] == serializer.data['generated_at']

  def test_retrieve__specified_report__returns_correct_store_data(
      self,
      client: APIClient,
      report_prefetched: "Report",
      report_summary_detail_url: Any,
  ) -> None:
    serializer = ReportSummarySerializer(
        report_prefetched,
        context={
            'week': str(default_pricing_week()),
            'year': str(default_pricing_year()),
        },
    )

    res = client.get(report_summary_detail_url(report_prefetched.id))

    assert res.status_code == status.HTTP_200_OK
    assert res.data['store'] == serializer.data['store']

  def test_retrieve__specified_report__returns_correct_item_data(
      self,
      client: APIClient,
      report_prefetched: "Report",
      report_summary_detail_url: Any,
  ) -> None:
    serializer = ReportSummarySerializer(
        report_prefetched,
        context={
            'week': str(default_pricing_week()),
            'year': str(default_pricing_year()),
        },
    )

    res = client.get(report_summary_detail_url(report_prefetched.id))

    assert res.status_code == status.HTTP_200_OK
    assert res.data['item'] == serializer.data['item']

  def test_retrieve__default_week_and_year__returns_none_for_missing_prices(
      self,
      client: APIClient,
      report_with_item: "Report",
      report_summary_detail_url: Any,
      report_price: "Price",
  ) -> None:
    expected_per_store = {str(s.id): None for s in report_with_item.store.all()}

    res = client.get(report_summary_detail_url(report_with_item.id))

    item_data = next(
        i for i in res.data['item'] if i['id'] == report_price.item.id
    )
    per_store = item_data['price']['selected_week']['per_store']
    assert per_store == expected_per_store

  def test_retrieve__specified_week_and_year__returns_correct_prices(
      self,
      client: APIClient,
      report_with_item: "Report",
      report_summary_detail_url: Any,
      report_price: "Price",
  ) -> None:
    expected_per_store: "dict[str, Optional[str]]" = {
        str(s.id): None for s in report_with_item.store.all()
    }
    expected_per_store[str(report_price.store.id)] = '99.99'

    res = client.get(
        report_summary_detail_url(report_with_item.id), {
            'week': 10,
            'year': 2025
        }
    )

    assert res.status_code == status.HTTP_200_OK
    item_data = next(
        i for i in res.data['item'] if i['id'] == report_price.item.id
    )
    per_store = item_data['price']['selected_week']['per_store']
    assert per_store == expected_per_store
