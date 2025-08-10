"""Admin for the Price model."""

from django.contrib import admin


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
  readonly_fields = (
      'last_52_weeks_average',
      'last_52_weeks_high',
      'last_52_weeks_low',
  )
  search_fields = ("item__name", "store__franchise__name")
