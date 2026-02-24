"""Tests for the ReportJsonViewSet."""

import pytest
from rest_framework import status

@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportJsonViewSet:
  """Tests for the ReportJsonViewSet."""

  def test_list(self, client, report, report_json_list_url):
    res = client.get(report_json_list_url())
    assert res.status_code == status.HTTP_200_OK

    # We can't easily check the whole data because generated_at changes
    # but we can check the keys and the number of reports
    assert len(res.data) == 1
    assert res.data[0]['id'] == report.id
    assert 'generated_at' in res.data[0]
    assert 'stores' in res.data[0]
    assert 'items' in res.data[0]

  def test_list__filter(self, client, report, report_json_list_url):
    res = client.get(report_json_list_url({'id': report.id}))
    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1

  def test_retrieve(self, client, report, report_json_detail_url):
    res = client.get(report_json_detail_url(report.id))
    assert res.status_code == status.HTTP_200_OK
    assert res.data['id'] == report.id
    assert 'generated_at' in res.data
    assert 'stores' in res.data
    assert 'items' in res.data
