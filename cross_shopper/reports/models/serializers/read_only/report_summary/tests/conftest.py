"""Test fixtures for the summary family of serializers for Reports."""

import decimal
from typing import TYPE_CHECKING
from unittest import mock

import pytest
from pricing.models import Price
from reports.models.serializers.read_only.report_summary.\
  item_price_current import (
    ReportSummaryCurrentItemPriceSerializerRO,
)

if TYPE_CHECKING:  # no cover
  from typing import Any, Callable, Dict

  from reports.models.report import Report
  AliasSerializerMockCreator = Callable[[str], mock.Mock]


@pytest.fixture
def report_context_2024(report_with_2024_prices: "Report") -> "Dict[str, Any]":
  return {
      "report": report_with_2024_prices,
      "year": 2024,
      "week": 1,
  }


@pytest.fixture
def report_context_2024_alternate(
    report_with_2024_prices: "Report",
) -> "Dict[str, Any]":
  return {
      "report": report_with_2024_prices,
      "year": 2024,
      "week": 2,
  }


@pytest.fixture
def report_context_no_prices(report: "Report") -> "Dict[str, Any]":
  return {
      "report": report,
      "year": 2024,
      "week": 1,
  }


@pytest.fixture
def create_mocked_price_aggregate_manager(
    monkeypatch: pytest.MonkeyPatch,
) -> "AliasSerializerMockCreator":

  def create(method_name: str) -> mock.Mock:
    instance = mock.Mock(return_value=10.0)
    monkeypatch.setattr(
        Price.aggregate_last_52_weeks,
        method_name,
        instance,
    )
    return instance

  return create


@pytest.fixture
def create_mocked_rs_serializer_price_getter(
    monkeypatch: pytest.MonkeyPatch,
) -> "AliasSerializerMockCreator":

  def create(method_name: str) -> mock.Mock:
    instance = mock.Mock(return_value={})
    instance.__name__ = f"get_{method_name}"
    monkeypatch.setattr(
        ReportSummaryCurrentItemPriceSerializerRO,
        f"get_{method_name}",
        instance,
    )
    return instance

  return create


@pytest.fixture
def report_summary_mocked_pricing_aggregate_attributes() -> "Dict[str, str]":
  return {
      "average": "10.5",
      "high": "15.0",
      "low": "5.0",
  }


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


@pytest.fixture
def report_with_2024_prices(report: "Report") -> "Report":
  stores = list(report.store.all())
  item = report.item.all()[0]
  num_stores = len(stores)

  for i in range(min(num_stores, 2)):
    Price.objects.create(
        item=item,
        store=stores[i],
        amount=decimal.Decimal(f"{(i + 1) * 10}.00"),
        year=2024,
        week=1,
    )

  return report
