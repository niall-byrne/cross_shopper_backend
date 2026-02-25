"""Report model list filter."""

from .franchise_filter import FranchiseFilter
from .item_filter import ItemFilter
from .location_filter import LocationFilter

report_list_filter = (
    ItemFilter,
    FranchiseFilter,
    LocationFilter,
    'is_testing_only',
)
