"""Admin for the Price model."""

from django.contrib import admin
from pricing.admin.list_filter.price import price_filter


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
  list_filter = price_filter
  ordering = ('-year', '-week')
  readonly_fields = (
      'last_52_weeks_average',
      'last_52_weeks_high',
      'last_52_weeks_low',
  )
  search_fields = ("item__name", "store__franchise__name")
