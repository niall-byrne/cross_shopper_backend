"""Admin models for the items app."""

from django.contrib import admin
from items.models import (
    Brand,
    Item,
    ItemScraperConfig,
    Packaging,
    PackagingContainer,
    PackagingUnit,
)
from . import filters
from .brand import BrandAdmin
from .item import ItemAdmin
from .item_scraper_config import ItemScraperConfigAdmin
from .packaging import PackagingAdmin
from .packaging_container import PackagingContainerAdmin
from .packaging_unit import PackagingUnitAdmin

admin.site.register(Brand, BrandAdmin)
admin.site.register(Item, ItemAdmin, list_filter=filters.item_filter)
admin.site.register(
    ItemScraperConfig,
    ItemScraperConfigAdmin,
    list_filter=filters.item_scraper_config_filter,
)
admin.site.register(
    Packaging,
    PackagingAdmin,
    list_filter=filters.packaging_filter,
)
admin.site.register(PackagingContainer, PackagingContainerAdmin)
admin.site.register(PackagingUnit, PackagingUnitAdmin)
