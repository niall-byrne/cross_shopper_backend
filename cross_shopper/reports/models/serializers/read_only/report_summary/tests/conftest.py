"""Test fixtures for the summary family of serializers for Reports."""

import decimal
from typing import TYPE_CHECKING
from unittest import mock

import pytest
from pricing.models import Price
from reports.models.report import Report

if TYPE_CHECKING:  # pragma: no cover
  from typing import Dict


@pytest.fixture
def report_with_2024_prices(report: Report) -> "Report":
  stores = list(report.store.all())
  item = report.item.all()[0]
  num_stores = len(stores)

  for i in range(min(num_stores, 2)):
    Price.objects.create(
        item=item,
        store=stores[i],
        amount=decimal.Decimal(f'{(i + 1) * 10}.00'),
        year=2024,
        week=1,
    )

  return report


@pytest.fixture
def report_summary_mocked_pricing_aggregate_attributes() -> "Dict[str, str]":
  return {
      'average': '10.5',
      'high': '15.0',
      'low': '5.0',
  }


# TODO: consider renaming
@pytest.fixture
def report_summary_mocked_pricing_aggregate_last_52_weeks_manager(
    report_summary_mocked_pricing_aggregate_attributes: "Dict[str, str]",
    monkeypatch: pytest.MonkeyPatch
) -> mock.Mock:
  manager_mock = mock.Mock()
  for attr, value in report_summary_mocked_pricing_aggregate_attributes.items():
    setattr(getattr(manager_mock, attr), "return_value", value)

  monkeypatch.setattr(Price, "aggregate_last_52_weeks", manager_mock)

  return manager_mock
