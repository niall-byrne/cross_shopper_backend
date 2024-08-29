"""Test the ReportStore model."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
  from reports.models import ReportStore


@pytest.mark.django_db
class TestReportStore:

  def test_str__returns_str_of_store(
      self,
      report_store: ReportStore,
  ) -> None:
    assert str(report_store) == str(report_store.store)
