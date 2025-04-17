"""Test the admin for the Price model."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # no cover
  from pricing.admin.price import PriceAdmin


class TestPriceAdmin:

  def test_instantiate__has_correct_fieldsets(
      self,
      price_admin: "PriceAdmin",
  ) -> None:
    assert price_admin.fieldsets == (
        (
            "Pricing",
            {
                "fields": ("amount", "item", "store")
            },
        ),
        (
            "Date",
            {
                "fields": ("week", "year"),
            },
        ),
        (
            "Historical Data", {
                "fields":
                    (
                        "last_52_weeks_average",
                        "last_52_weeks_high",
                        "last_52_weeks_low",
                    ),
            }
        ),
    )

  def test_instantiate__has_correct_readonly_fields(
      self,
      price_admin: "PriceAdmin",
  ) -> None:
    assert price_admin.readonly_fields == (
        "last_52_weeks_average",
        "last_52_weeks_high",
        "last_52_weeks_low",
    )
