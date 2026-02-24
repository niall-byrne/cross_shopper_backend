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
from .brand import BrandAdmin
from .item import ItemAdmin
from .item_scraper_config import ItemScraperConfigAdmin
from .packaging import PackagingAdmin
from .packaging_container import PackagingContainerAdmin
from .packaging_unit import PackagingUnitAdmin

admin.site.register(Brand, BrandAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemScraperConfig, ItemScraperConfigAdmin)
admin.site.register(Packaging, PackagingAdmin)
admin.site.register(PackagingContainer, PackagingContainerAdmin)
admin.site.register(PackagingUnit, PackagingUnitAdmin)
