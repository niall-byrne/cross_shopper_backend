"""Store model list filter."""

from .franchise_filter import FranchiseFilter
from .location_filter import LocationFilter

store_filter = (FranchiseFilter, LocationFilter)
