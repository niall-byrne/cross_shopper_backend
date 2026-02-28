"""Tests for the ReportSummaryFilter."""

import pytest
from reports.models.factories.report import ReportFactory
from ..filters import ReportSummaryFilter


@pytest.mark.django_db
class TestReportSummaryFilter:
  """Tests for the ReportSummaryFilter."""

  def test_filter__by_name__returns_filtered_queryset(self):
    report1 = ReportFactory(name="Report One")
    _report2 = ReportFactory(name="Report Two")
    data = {"name": "Report One"}
    filterset = ReportSummaryFilter(data, queryset=report1.__class__.objects.all())
    assert filterset.qs.count() == 1
    assert filterset.qs[0].id == report1.id

  def test_filter__by_testing__returns_filtered_queryset(self):
    report1 = ReportFactory(is_testing=True)
    _report2 = ReportFactory(is_testing=False)
    data = {"is_testing": "True"}
    filterset = ReportSummaryFilter(data, queryset=report1.__class__.objects.all())
    assert filterset.qs.count() == 1
    assert filterset.qs[0].id == report1.id
