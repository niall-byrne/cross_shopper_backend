"""Admin for the price model."""

from django.contrib import admin
from pricing.admin.filters import price_filter


class PriceAdmin(admin.ModelAdmin):
  fieldsets = (
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
  readonly_fields = (
      'last_52_weeks_average',
      'last_52_weeks_high',
      'last_52_weeks_low',
  )
  search_fields = ("item__name", "store__franchise__name")
  list_filter = price_filter
  ordering = ('-year', '-week')
