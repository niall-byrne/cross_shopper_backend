"""Admin for the report store model."""

from django.contrib import admin
from reports.admin import filters
from reports.models import ReportStore


class ReportStoreAdmin(admin.ModelAdmin[ReportStore]):
  search_fields = (
      "store__address__locality__name",
      "store__franchise__name",
  )
  list_filter = filters.report_store_filter
  ordering = ('report__name', 'store__franchise__name')
