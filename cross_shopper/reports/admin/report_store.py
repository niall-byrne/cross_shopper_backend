"""Admin models for the Report model."""

from django.contrib import admin
from reports.models import Report


class ReportStoreAdmin(admin.ModelAdmin[Report]):
  ordering = ("store__franchise__name", "store")
  search_fields = (
      "store__address__locality__name",
      "store__franchise__name",
  )
