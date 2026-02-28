"""Tests for the ReportJsonViewSet."""

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
class TestReportJsonViewSet:
  """Tests for the ReportJsonViewSet."""

  def test_list(self, client, report, report_summary_list_url):
    res = client.get(report_summary_list_url())
    assert res.status_code == status.HTTP_200_OK

    assert len(res.data) == 1
    assert res.data[0]['id'] == report.id
    assert 'generated_at' in res.data[0]
    assert 'stores' in res.data[0]
    assert 'items' in res.data[0]

  def test_list__filter_by_id(self, client, report, report_summary_list_url):
    res = client.get(report_summary_list_url({'id': report.id}))
    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1

  def test_retrieve(self, client, report, report_summary_detail_url):
    res = client.get(report_summary_detail_url(report.id))
    assert res.status_code == status.HTTP_200_OK
    assert res.data['id'] == report.id
    assert 'generated_at' in res.data
    assert 'stores' in res.data
    assert 'items' in res.data

  def test_retrieve__with_week_year_params(
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

    # Request without params (default week/year)
    res = client.get(report_summary_detail_url(report.id))
    item_data = next(i for i in res.data['items'] if i['id'] == item.id)
    assert item_data['prices'][str(store.id)] is None

    # Request with params
    res = client.get(
        report_summary_detail_url(report.id), {
            'week': 10,
            'year': 2025
        }
    )
    assert res.status_code == status.HTTP_200_OK
    item_data = next(i for i in res.data['items'] if i['id'] == item.id)
    assert item_data['prices'][str(store.id)] == '99.99'
