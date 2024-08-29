"""Admin models for the reports app."""

from django.contrib import admin
from reports.admin.report import ReportAdmin
from reports.admin.report_store import ReportStoreAdmin
from reports.models import Report, ReportStore

admin.site.register(Report, ReportAdmin)
admin.site.register(ReportStore, ReportStoreAdmin)
