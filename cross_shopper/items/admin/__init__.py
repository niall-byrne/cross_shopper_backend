"""Admin models for the items app."""

from django.contrib import admin
from items.admin.brand import BrandAdmin
from items.admin.item import ItemAdmin
from items.admin.item_scraper_config import ItemScraperConfigAdmin
from items.admin.packaging import PackagingAdmin
from items.admin.packaging_container import PackagingContainerAdmin
from items.admin.packaging_unit import PackagingUnitAdmin
from items.models import (
    Brand,
    Item,
    ItemScraperConfig,
    Packaging,
    PackagingContainer,
    PackagingUnit,
)

admin.site.register(Brand, BrandAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemScraperConfig, ItemScraperConfigAdmin)
admin.site.register(Packaging, PackagingAdmin)
admin.site.register(PackagingContainer, PackagingContainerAdmin)
admin.site.register(PackagingUnit, PackagingUnitAdmin)
