"""Tests for the ReportSummaryViewSet."""

import decimal
from typing import Any

import pytest
from items.models import Item
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

  def test_list__all_reports__correct_representation(
      self,
      client: APIClient,
      report: Report,
      report_summary_list_url: Any,
  ) -> None:
    res = client.get(report_summary_list_url())
    serializer = ReportSummarySerializer(report)

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1
    assert res.data[0]['id'] == report.id
    assert res.data[0]['name'] == report.name
    # Check that generated_at exists and is a string
    assert isinstance(res.data[0]['generated_at'], str)
    # Check that item and store are present
    assert 'item' in res.data[0]
    assert 'store' in res.data[0]

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
    from api.views.report_summary.qs import qs_item

    # We need to ensure the report in the serializer context has the same data
    # as what's returned by the ViewSet's prefetched queryset.
    from django.db.models import Prefetch
    from pricing.models.defaults.default_pricing_week import (
      default_pricing_week,
    )
    from pricing.models.defaults.default_pricing_year import (
      default_pricing_year,
    )
    qs = Report.objects.filter(id=report.id).prefetch_related(
        'store',
        Prefetch('item', queryset=qs_item()),
    )
    report_prefetched = qs.get()
    serializer = ReportSummarySerializer(
        report_prefetched,
        context={
            'week': default_pricing_week(),
            'year': default_pricing_year(),
        },
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data['id'] == report.id
    assert res.data['name'] == report.name
    # Verify that the API returns items in the correct order (database-level).
    assert res.data['item'] == serializer.data['item']
    assert res.data['store'] == serializer.data['store']

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

  def test_retrieve__specified_week_and_year__correct_prices_returned(
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
