"""Admin models for the items app."""

from django.contrib import admin
from items.models import (
    Brand,
    Item,
    Packaging,
    PackagingContainer,
    PackagingUnit,
)
from . import filters
from .brand import BrandAdmin
from .item import ItemAdmin, ItemScraperConfig
from .packaging import PackagingAdmin
from .packaging_container import PackagingContainerAdmin
from .packaging_unit import PackagingUnitAdmin

admin.site.register(Brand, BrandAdmin)
admin.site.register(Item, ItemAdmin, list_filter=filters.item_filter)
admin.site.register(
    ItemScraperConfig, list_filter=filters.scraper_config_filter
)
admin.site.register(
    Packaging, PackagingAdmin, list_filter=filters.packaging_filter
)
admin.site.register(PackagingContainer, PackagingContainerAdmin)
admin.site.register(PackagingUnit, PackagingUnitAdmin)
