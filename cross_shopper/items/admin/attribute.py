"""Admin for the attribute model."""

from django.contrib import admin
from items.admin.list_displays.attribute import attribute_list_display
from items.admin.list_filters.attribute import attribute_list_filter
from items.models import Attribute
from utilities.admin.list_displays.decorator import generate_list_display


@generate_list_display(attribute_list_display)
class AttributeAdmin(admin.ModelAdmin[Attribute]):
  list_filter = attribute_list_filter
  ordering = ("name",)
