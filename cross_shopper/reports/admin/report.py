"""Admin models for the Report model."""

from django.contrib import admin
from reports.admin.list_filter.report import report_list_filter
from reports.models import Report, ReportStore


class ReportStoreInline(admin.TabularInline[ReportStore, ReportStore]):
  model = ReportStore
  extra = 0


class ReportAdmin(admin.ModelAdmin[Report]):
  fieldsets = (
      (
          "IDENTIFICATION",
          {
              "fields": ('name', 'user', 'is_testing')
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
  list_filter = report_list_filter
  ordering = ('name',)
