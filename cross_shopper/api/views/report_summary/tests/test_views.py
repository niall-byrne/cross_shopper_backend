"""Tests for the ReportSummaryViewSet."""

import decimal
from typing import Any, Dict

import pytest
from pricing.models.factories.pricing import PriceFactory
from rest_framework import status
from rest_framework.test import APIClient
from reports.models import Report
from items.models import Item


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportSummaryViewSet:
  """Tests for the ReportSummaryViewSet."""

  def test_list(
      self, client: APIClient, report: Report, report_summary_list_url: Any
  ) -> None:
    """Test the list endpoint of ReportSummaryViewSet."""
    res = client.get(report_summary_list_url())
    assert res.status_code == status.HTTP_200_OK

    assert len(res.data) == 1
    assert res.data[0]['id'] == report.id
    assert 'generated_at' in res.data[0]
    assert 'store' in res.data[0]
    assert 'item' in res.data[0]

  def test_list__filter_by_id(
      self, client: APIClient, report: Report, report_summary_list_url: Any
  ) -> None:
    """Test filtering the list endpoint by ID."""
    res = client.get(report_summary_list_url({'id': report.id}))
    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1

  def test_retrieve(
      self, client: APIClient, report: Report, report_summary_detail_url: Any
  ) -> None:
    """Test the detail endpoint of ReportSummaryViewSet."""
    res = client.get(report_summary_detail_url(report.id))
    assert res.status_code == status.HTTP_200_OK
    assert res.data['id'] == report.id
    assert 'generated_at' in res.data
    assert 'store' in res.data
    assert 'item' in res.data

  def test_retrieve__with_week_year_params(
      self, client: APIClient, report: Report, report_summary_detail_url: Any,
      item: Item
  ) -> None:
    """Test the detail endpoint with week and year query parameters."""
    report.item.add(item)
    stores = list(report.store.all())
    store = stores[0]
    PriceFactory(
        item=item,
        store=store,
        amount=decimal.Decimal('99.99'),
        year=2025,
        week=10,
    )

    # Request without params (default week/year)
    res = client.get(report_summary_detail_url(report.id))
    item_data = next(i for i in res.data['item'] if i['id'] == item.id)
    per_store = item_data['price']['selected_week']['per_store']
    assert str(store.id) in per_store
    assert per_store[str(store.id)] is None

    # Request with params
    res = client.get(
        report_summary_detail_url(report.id), {
            'week': 10,
            'year': 2025
        }
    )
    assert res.status_code == status.HTTP_200_OK
    item_data = next(i for i in res.data['item'] if i['id'] == item.id)
    per_store = item_data['price']['selected_week']['per_store']
    assert str(store.id) in per_store
    assert per_store[str(store.id)] == '99.99'
