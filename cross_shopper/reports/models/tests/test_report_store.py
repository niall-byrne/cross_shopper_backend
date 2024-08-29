"""Test the ReportStore model."""

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:  # no cover
  from reports.models import ReportStore


@pytest.mark.django_db
class TestReportStore:

  def test_str__returns_str_of_store(
      self,
      report_store: "ReportStore",
  ) -> None:
    assert str(report_store) == str(report_store.store)
