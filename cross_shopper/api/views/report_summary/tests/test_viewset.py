"""Tests for the ReportSummaryViewSet."""

import decimal
import pytest
from pricing.models.factories.pricing import PriceFactory
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportSummaryViewSet:
  """Tests for the ReportSummaryViewSet."""

  def test_list__all_clients__200_ok(self, client, report, report_summary_list_url):
    res = client.get(report_summary_list_url(report.id))
    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1
    assert res.data[0]['id'] == report.id
    assert 'stores' in res.data[0]
    assert 'items' in res.data[0]

  def test_retrieve__all_clients__200_ok(self, client, report, report_summary_detail_url):
    res = client.get(report_summary_detail_url(report.id))
    assert res.status_code == status.HTTP_200_OK
    assert res.data['id'] == report.id

  def test_retrieve__with_params__uses_params_in_context(
      self, client, report, report_summary_detail_url, item
  ):
    report.item.add(item)
    store = report.store.all()[0]
    PriceFactory(
        item=item,
        store=store,
        amount=decimal.Decimal('99.99'),
        year=2025,
        week=10,
    )

    res = client.get(
        report_summary_detail_url(report.id),
        {'week': 10, 'year': 2025}
    )
    assert res.status_code == status.HTTP_200_OK
    assert int(res.data['week']) == 10
    assert int(res.data['year']) == 2025
    item_data = next(i for i in res.data['items'] if i['id'] == item.id)
    assert item_data['price']['selected_week']['per_store'][str(store.id)] == '99.99'
