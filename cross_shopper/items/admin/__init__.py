"""Admin models for the items app."""

from django.contrib import admin
from items.models import (
    Brand,
    Item,
    Packaging,
    PackagingContainer,
    PackagingUnit,
)
from .item import ItemAdmin, ItemScraperConfig
from .packaging_container import PackagingContainerAdmin
from .packaging_unit import PackagingUnitAdmin

admin.site.register(Brand)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemScraperConfig)
admin.site.register(Packaging)
admin.site.register(PackagingContainer, PackagingContainerAdmin)
admin.site.register(PackagingUnit, PackagingUnitAdmin)
