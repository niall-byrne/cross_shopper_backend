"""Admin for the item model."""

from typing import TYPE_CHECKING

from constance import config
from django.contrib import admin
from items.admin.inlines.item import item_inlines
from items.admin.list_displays.item import item_list_display
from items.admin.list_filters.item import item_list_filter
from items.admin.mixins.price_group_members import PriceGroupMembersAdminMixin
from items.models import Brand, Item, Packaging
from reports.models import Report
from utilities.admin.list_displays.decorator import generate_list_display

if TYPE_CHECKING:  # no cover
  from typing import Any

  from django.db.models import ForeignKey
  from django.forms import ModelChoiceField, ModelForm
  from django.http import HttpRequest


@generate_list_display(item_list_display)
class ItemAdmin(admin.ModelAdmin[Item], PriceGroupMembersAdminMixin):
  fieldsets = (
      (
          "IDENTIFICATION",
          {
              "fields": ('name', 'brand')
          },
      ), (
          "PACKAGING",
          {
              "fields": ('packaging',),
          },
      ), (
          "PRICE COMPARISONS",
          {
              "fields": ('price_group', 'price_group_members'),
          },
      ), (
          "CERTIFICATIONS",
          {
              "fields": (
                  'is_non_gmo',
                  'is_organic',
              ),
          },
      )
  )
  inlines = item_inlines
  list_filter = item_list_filter
  ordering = (
      'name',
      'brand__name',
      'is_organic',
      'packaging__container',
      'packaging__quantity',
  )
  readonly_fields = ('price_group_members',)
  search_fields = (
      'name',
      'attribute__name',
      'brand__name',
  )

  def price_group_members(self, obj: Item) -> str:
    """Return an HTML representation of the price_group members."""
    return self.members(obj.price_group)

  def formfield_for_foreignkey(
      self,
      db_field: "ForeignKey[Any, Any]",
      request: "HttpRequest",
      **kwargs: "Any",
  ) -> "ModelChoiceField":
    """Return a form field for a foreign key with custom queryset ordering."""
    if db_field.name == "brand":
      kwargs["queryset"] = Brand.objects.order_by('name')
    if db_field.name == "packaging":
      kwargs["queryset"] = Packaging.objects.order_by(
          'container__name',
          'quantity',
      )
    return super().formfield_for_foreignkey(db_field, request, **kwargs)

  def save_model(
      self,
      request: "HttpRequest",
      obj: "Item",
      form: "ModelForm[Item]",
      change: "bool",
  ) -> None:
    """Given a model instance save it to the database."""
    super().save_model(request, obj, form, change)

    if config.ADMIN_AUTO_ATTACH_ITEMS_TO_REPORTS:
      for report in Report.objects.filter(is_testing=False):
        report.item.add(obj)
