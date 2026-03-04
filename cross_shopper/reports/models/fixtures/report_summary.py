"""Fixtures for building Report model summaries."""

from typing import TYPE_CHECKING

import pytest
from api.views.report_summary.qs import qs_item
from django.db.models import Prefetch
from reports.models import Report

if TYPE_CHECKING:  # no cover
  from typing import Callable

  AliasReportPrefetcher = Callable[[Report], Report]


@pytest.fixture
def report_prefetcher() -> "AliasReportPrefetcher":

  def as_prefetched(report: "Report") -> "Report":
    return Report.objects.filter(id=report.pk).prefetch_related(
        Prefetch(
            'item',
            queryset=qs_item(),
        )
    ).get(id=report.pk)

  return as_prefetched


@pytest.fixture
def report_prefetched(
    report: "Report",
    report_prefetcher: "AliasReportPrefetcher",
) -> "Report":
  return report_prefetcher(report)


@pytest.fixture
def report_prefetched_alternate(
    report_alternate: "Report",
    report_prefetcher: "AliasReportPrefetcher",
) -> "Report":
  return report_prefetcher(report_alternate)


@pytest.fixture
def report_prefetched_testing(
    report_testing: "Report",
    report_prefetcher: "AliasReportPrefetcher",
) -> "Report":
  return report_prefetcher(report_testing)
