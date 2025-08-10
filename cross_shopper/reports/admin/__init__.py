"""Admin models for the reports app."""

from django.contrib import admin
from reports.models import Report, ReportStore


class ReportStoreInline(admin.TabularInline[ReportStore, ReportStore]):
  model = ReportStore
  extra = 0


class ReportAdmin(admin.ModelAdmin[Report]):
  fieldsets = (
      (
          "IDENTIFICATION",
          {
              "fields": ('name', 'user', 'is_testing_only')
          },
      ),
      (
          "ITEMS",
          {
              "fields": ('item',)
          },
      ),
  )
  filter_horizontal = [
      'item',
  ]
  inlines = [ReportStoreInline]


class ReportStoreAdmin(admin.ModelAdmin[ReportStore]):
  search_fields = (
      "store__address__locality__name",
      "store__franchise__name",
  )


admin.site.register(Report, ReportAdmin)
admin.site.register(ReportStore, ReportStoreAdmin)
