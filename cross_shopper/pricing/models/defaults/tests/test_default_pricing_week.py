"""Test the default_pricing_week function."""
from datetime import datetime, timedelta, timezone

import pytest
from freezegun import freeze_time
from pricing.models import Price
from pricing.models.defaults import default_pricing_week
from .scenarios import eoy_boundary_scenarios


class TestDefaultPricingWeek:

  mocked_date = datetime(2024, 9, 2, tzinfo=timezone.utc)

  @pytest.mark.parametrize(
      "weekday",
      list(range(0, Price.DAY_OF_WEEK_FOR_PRICING)),
  )
  def test__call__before_prices_change__returns_expected_value(
      self,
      weekday: int,
  ) -> None:
    with freeze_time(self.mocked_date + timedelta(days=weekday)):

      assert default_pricing_week.default_pricing_week() == \
          self.mocked_date.isocalendar().week

  @pytest.mark.parametrize(
      "weekday",
      list(range(Price.DAY_OF_WEEK_FOR_PRICING, 7)),
  )
  def test__call__after_prices_change__returns_expected_value(
      self,
      weekday: int,
  ) -> None:
    with freeze_time(self.mocked_date + timedelta(days=weekday)):

      assert default_pricing_week.default_pricing_week() == \
          self.mocked_date.isocalendar().week + 1

  @eoy_boundary_scenarios
  def test__call__eoy_boundary_condition__returns_expected_value(
      self,
      edge_case_datetime: datetime,
      iso_week_wrapping: bool,
  ) -> None:
    with freeze_time(edge_case_datetime):

      assert default_pricing_week.default_pricing_week() == \
          1 if iso_week_wrapping else edge_case_datetime.isocalendar().week
