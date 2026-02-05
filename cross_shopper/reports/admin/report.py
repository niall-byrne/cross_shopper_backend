"""Admin models for the Report model."""

from django.contrib import admin
from reports.admin.inlines.report import report_inlines
from reports.admin.list_filters.report import report_list_filter
from reports.models import Report


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
  inlines = report_inlines
  list_filter = report_list_filter
  ordering = ('name',)
