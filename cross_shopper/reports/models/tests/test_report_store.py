"""Test the ReportStore model."""

import pytest
from reports.models import ReportStore


@pytest.mark.django_db
class TestReportStore:

  def test_str__returns_str_of_store(
      self,
      report_store: ReportStore,
  ) -> None:
    assert str(report_store) == str(report_store.store)
