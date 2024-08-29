"""Item admin model ReportStore inline."""

from django.contrib import admin
from reports.models import Report, ReportStore


class ReportStoreInline(
    admin.StackedInline[ReportStore, Report],
):
  extra = 0
  ordering = (
      'store__franchise__name',
      'store__address',
  )
  model = ReportStore
  verbose_name = 'Report Stores'
  verbose_name_plural = 'Report Stores'
