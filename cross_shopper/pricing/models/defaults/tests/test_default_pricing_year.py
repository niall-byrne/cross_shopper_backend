"""Test the default_pricing_year function."""

from datetime import datetime

from freezegun import freeze_time
from .. import default_pricing_year
from .scenarios import eoy_boundary_scenarios, non_boundary_scenarios


class TestDefaultPricingYear:
  """Test the default_pricing_year function."""

  @non_boundary_scenarios
  def test__call__returns_expected_value(
      self,
      test_datetime: datetime,
  ) -> None:
    with freeze_time(test_datetime):

      assert default_pricing_year.default_pricing_year() == test_datetime.year

  @eoy_boundary_scenarios
  def test__call__eoy_boundary_condition__returns_expected_value(
      self,
      edge_case_datetime: datetime,
      iso_week_wrapping: bool,
  ) -> None:
    with freeze_time(edge_case_datetime):

      assert default_pricing_year.default_pricing_year() == \
          edge_case_datetime.year + (1 if iso_week_wrapping else 0)
