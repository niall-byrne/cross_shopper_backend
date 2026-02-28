"""Admin models for the Report model."""

from django.contrib import admin
from reports.admin.list_displays.report_store import report_store_list_display
from reports.admin.list_filters.report_store import report_store_list_filter
from reports.models import Report
from utilities.admin.list_displays.decorator import generate_list_display


@generate_list_display(report_store_list_display)
class ReportStoreAdmin(admin.ModelAdmin[Report]):
  list_filter = report_store_list_filter
  ordering = ("store__franchise__name", "store")
  search_fields = (
      "store__address__locality__name",
      "store__franchise__name",
  )
