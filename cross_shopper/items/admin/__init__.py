"""Admin models for the items app."""

from django.contrib import admin
from items.admin.item import ItemAdmin
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

admin.site.register(Brand)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemScraperConfig)
admin.site.register(Packaging)
admin.site.register(PackagingContainer, PackagingContainerAdmin)
admin.site.register(PackagingUnit, PackagingUnitAdmin)
