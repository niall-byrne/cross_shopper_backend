"""Test the AggregateLast52WeeksManager class."""
import decimal
from typing import TYPE_CHECKING

import pytest
from freezegun import freeze_time
from pricing.models import Price
from .scenarios import eoy_boundary_scenarios

if TYPE_CHECKING:  # no cover
  from pricing.models.fixtures.pricing import (
      AliasCreateLast52PriceBatchFromReport,
  )
  from reports.models import Report


@pytest.mark.django_db
class TestAggregateLast52WeeksManager:

  def test_average__without_pricing__returns_none(
      self,
      report: "Report",
  ) -> None:
    assert Price.aggregate_last_52_weeks.average(
        report.item.all()[0],
        report.store.all(),
    ) is None

  @eoy_boundary_scenarios
  def test_average__with_pricing__returns_correct_value(
      self,
      test_datetime: str,
      report: "Report",
      create_last_52_price_batch_from_report:
      "AliasCreateLast52PriceBatchFromReport",
  ) -> None:
    with freeze_time(test_datetime):

      price_batch = create_last_52_price_batch_from_report(report)

      expected_average = sum(
          price.amount
          for price in price_batch
          if price.last_52_weeks_average is not None
      ) / decimal.Decimal(len(price_batch))

      assert Price.aggregate_last_52_weeks.average(
          price_batch[0].item,
          report.store.all(),
      ) == expected_average.quantize(
          decimal.Decimal(".01"),
          rounding=decimal.ROUND_HALF_UP,
      )

  def test_high__without_pricing__returns_none(
      self,
      report: "Report",
  ) -> None:
    assert Price.aggregate_last_52_weeks.high(
        report.item.all()[0],
        report.store.all(),
    ) is None

  @eoy_boundary_scenarios
  def test_high__with_pricing__returns_correct_value(
      self,
      test_datetime: str,
      report: "Report",
      create_last_52_price_batch_from_report:
      "AliasCreateLast52PriceBatchFromReport",
  ) -> None:
    with freeze_time(test_datetime):

      price_batch = create_last_52_price_batch_from_report(report)

      assert Price.aggregate_last_52_weeks.high(
          price_batch[0].item,
          report.store.all(),
      ) == max(
          [
              price.amount
              for price in price_batch
              if price.last_52_weeks_high is not None
          ]
      )

  def test_low__without_pricing__returns_none(
      self,
      report: "Report",
  ) -> None:
    assert Price.aggregate_last_52_weeks.low(
        report.item.all()[0],
        report.store.all(),
    ) is None

  @eoy_boundary_scenarios
  def test_low__with_pricing__returns_correct_value(
      self,
      test_datetime: str,
      report: "Report",
      create_last_52_price_batch_from_report:
      "AliasCreateLast52PriceBatchFromReport",
  ) -> None:
    with freeze_time(test_datetime):

      price_batch = create_last_52_price_batch_from_report(report)

      assert Price.aggregate_last_52_weeks.low(
          price_batch[0].item,
          report.store.all(),
      ) == min(
          [
              price.amount
              for price in price_batch
              if price.last_52_weeks_low is not None
          ]
      )
