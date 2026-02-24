"""Price model list filter."""

from .brand_filter import BrandFilter
from .franchise_filter import FranchiseFilter
from .item_filter import ItemFilter
from .location_filter import LocationFilter
from .year_filter import YearFilter

price_filter = (
    ItemFilter,
    BrandFilter,
    FranchiseFilter,
    LocationFilter,
    YearFilter,
    'week',
)
