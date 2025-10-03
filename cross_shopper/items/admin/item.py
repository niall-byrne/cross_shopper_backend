"""Admin for the item model."""

from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib import admin
from items.models import Brand, Item, ItemScraperConfig, Packaging
from reports.models import Report

if TYPE_CHECKING:  # no cover
  from typing import Any

  from django.db.models import ForeignKey
  from django.forms import ModelForm
  from django.http import HttpRequest


class ItemScraperConfigInline(
    admin.StackedInline[ItemScraperConfig, ItemScraperConfig],
):
  model = ItemScraperConfig


class ItemAdmin(admin.ModelAdmin[Item]):
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
          "CHARACTERISTICS",
          {
              "fields": (
                  'is_non_gmo',
                  'is_organic',
              ),
          },
      )
  )
  inlines = [ItemScraperConfigInline]
  ordering = (
      'name',
      'brand__name',
      'is_organic',
      'packaging__container',
      'packaging__quantity',
  )
  search_fields = ('name', 'brand__name')

  def formfield_for_foreignkey(
      self,
      db_field: "ForeignKey",
      request: "HttpRequest",
      **kwargs: "Any",
  ):
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
      form: "ModelForm",
      change: "bool",
  ):
    """Given a model instance save it to the database."""
    super().save_model(request, obj, form, change)

    if settings.ADMIN_AUTO_ATTACH_ITEMS_TO_REPORTS:
      for report in Report.objects.filter(is_testing_only=False):
        report.item.add(obj)
