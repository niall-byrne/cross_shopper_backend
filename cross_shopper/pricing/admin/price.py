"""Admin for the Price model."""

from django.contrib import admin
from pricing.admin.list_display.price import price_list_display
from pricing.admin.list_filter.price import price_list_filter
from utilities.admin.list_display import generate_list_display


@generate_list_display(price_list_display)
class PriceAdmin(admin.ModelAdmin):
  fieldsets = (
      (
          'Pricing',
          {
              'fields': ('amount', 'item', 'store')
          },
      ),
      (
          'Date',
          {
              'fields': ('week', 'year'),
          },
      ),
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
  list_filter = price_list_filter
  ordering = (
      '-year',
      '-week',
      'item__name',
      'store__franchise__name',
  )
  readonly_fields = (
      'last_52_weeks_average',
      'last_52_weeks_high',
      'last_52_weeks_low',
  )
  search_fields = ("item__name", "store__franchise__name")
