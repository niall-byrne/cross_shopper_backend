"""Admin models for the pricing app."""

from django.contrib import admin
from ..models import Price


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


admin.site.register(Price, PriceAdmin)
