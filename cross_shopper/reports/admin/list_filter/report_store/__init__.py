"""ReportStore model list filter."""

from .franchise_filter import FranchiseFilter
from .report_filter import ReportFilter

report_store_filter = (
    ReportFilter,
    FranchiseFilter,
    'report__is_testing_only',
)
