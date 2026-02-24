"""Test the admin for the Price model."""

from django.contrib import admin
from pricing.admin import PriceAdmin, filters


class TestPriceAdmin:
  """Test the PriceAdmin class."""

  def test_instantiate__inheritance(
      self,
      price_admin: PriceAdmin,
  ) -> None:
    assert isinstance(price_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_fieldsets(
      self,
      price_admin: PriceAdmin,
  ) -> None:
    assert price_admin.fieldsets == (
        ('Pricing', {
            'fields': ('amount', 'item', 'store')
        }),
        ('Date', {
            'fields': ('week', 'year'),
        }),
        (
            'Historical Data', {
                'fields':
                    (
                        'last_52_weeks_average',
                        'last_52_weeks_high',
                        'last_52_weeks_low',
                    ),
            }
        ),
    )

  def test_instantiate__has_correct_readonly_fields(
      self,
      price_admin: PriceAdmin,
  ) -> None:
    assert price_admin.readonly_fields == (
        'last_52_weeks_average',
        'last_52_weeks_high',
        'last_52_weeks_low',
    )

  def test_instantiate__has_correct_search_fields(
      self,
      price_admin: PriceAdmin,
  ) -> None:
    assert price_admin.search_fields == ("item__name", "store__franchise__name")

  def test_instantiate__has_correct_list_filter(
      self,
      price_admin: PriceAdmin,
  ) -> None:
    assert price_admin.list_filter == filters.price_filter

  def test_instantiate__ordering(self, price_admin: PriceAdmin) -> None:
    assert price_admin.ordering == ('-year', '-week')
