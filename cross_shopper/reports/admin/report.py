"""Admin for the report model."""

from django.contrib import admin
from reports.models import Report, ReportStore

from . import filters


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
  list_filter = filters.report_filter
  ordering = ('name',)
