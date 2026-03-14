"""Admin models for the items app."""

from django.contrib import admin
from items.admin.attribute import AttributeAdmin
from items.admin.brand import BrandAdmin
from items.admin.item import ItemAdmin
from items.admin.item_attribute import ItemAttributeAdmin
from items.admin.item_scraper_config import ItemScraperConfigAdmin
from items.admin.packaging import PackagingAdmin
from items.admin.packaging_container import PackagingContainerAdmin
from items.admin.packaging_unit import PackagingUnitAdmin
from items.admin.price_group import PriceGroupAdmin
from items.admin.price_group_attribute import PriceGroupAttributeAdmin
from items.models import (
    Attribute,
    Brand,
    Item,
    ItemAttribute,
    ItemScraperConfig,
    Packaging,
    PackagingContainer,
    PackagingUnit,
    PriceGroup,
    PriceGroupAttribute,
)

admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemAttribute, ItemAttributeAdmin)
admin.site.register(ItemScraperConfig, ItemScraperConfigAdmin)
admin.site.register(Packaging, PackagingAdmin)
admin.site.register(PackagingContainer, PackagingContainerAdmin)
admin.site.register(PackagingUnit, PackagingUnitAdmin)
admin.site.register(PriceGroup, PriceGroupAdmin)
admin.site.register(PriceGroupAttribute, PriceGroupAttributeAdmin)
