"""Admin models for the reports app."""

from django.contrib import admin
from reports.models import Report, ReportStore
from .report import ReportAdmin
from .report_store import ReportStoreAdmin

admin.site.register(Report, ReportAdmin)
admin.site.register(ReportStore, ReportStoreAdmin)
