"""Admin models for the reports app."""

from django.contrib import admin
from reports.models import Report, ReportStore
from . import filters
from .report import ReportAdmin
from .report_store import ReportStoreAdmin

admin.site.register(Report, ReportAdmin, list_filter=filters.report_filter)
admin.site.register(
    ReportStore, ReportStoreAdmin, list_filter=filters.report_store_filter
)
