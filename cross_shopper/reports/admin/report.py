"""Admin models for the Report model."""

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
              "fields": ('name', 'user')
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
