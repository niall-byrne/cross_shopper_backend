"""Tests for the ReportSummaryViewSet."""

import decimal
from typing import Any, Dict

import pytest
from pricing.models.factories.pricing import PriceFactory
from rest_framework import status
from rest_framework.test import APIClient
from reports.models import Report
from items.models import Item
from reports.models.serializers.report_summary.report import (
    ReportSummarySerializer,
)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportSummaryViewSet:
  """Tests for the ReportSummaryViewSet."""

  def test_list__all_reports__correct_representation(
      self,
      client: APIClient,
      report: Report,
      report_summary_list_url: Any,
  ) -> None:
    res = client.get(report_summary_list_url())

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1
    assert res.data[0]['id'] == report.id
    assert res.data[0]['name'] == report.name

  def test_list__filter_by_id__one_report(
      self,
      client: APIClient,
      report: Report,
      report_summary_list_url: Any,
  ) -> None:
    res = client.get(report_summary_list_url({'id': report.id}))

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1

  def test_retrieve__specified_report__correct_representation(
      self,
      client: APIClient,
      report: Report,
      report_summary_detail_url: Any,
  ) -> None:
    res = client.get(report_summary_detail_url(report.id))

    assert res.status_code == status.HTTP_200_OK
    assert res.data['id'] == report.id
    assert res.data['name'] == report.name

  def test_retrieve__default_params__no_prices_found(
      self,
      client: APIClient,
      report_with_item: Report,
      report_summary_detail_url: Any,
      item: Item,
  ) -> None:
    store = list(report_with_item.store.all())[0]
    PriceFactory(
        item=item,
        store=store,
        amount=decimal.Decimal('99.99'),
        year=2025,
        week=10,
    )
    res = client.get(report_summary_detail_url(report_with_item.id))
    item_data = next(i for i in res.data['item'] if i['id'] == item.id)
    per_store = item_data['price']['selected_week']['per_store']

    assert str(store.id) in per_store
    assert per_store[str(store.id)] is None

  def test_retrieve__week_year_params__correct_prices(
      self,
      client: APIClient,
      report_with_item: Report,
      report_summary_detail_url: Any,
      item: Item,
  ) -> None:
    store = list(report_with_item.store.all())[0]
    PriceFactory(
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
    item_data = next(i for i in res.data['item'] if i['id'] == item.id)
    per_store = item_data['price']['selected_week']['per_store']

    assert res.status_code == status.HTTP_200_OK
    assert str(store.id) in per_store
    assert per_store[str(store.id)] == '99.99'
