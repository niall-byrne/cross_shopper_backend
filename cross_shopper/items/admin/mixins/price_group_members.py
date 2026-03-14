"""An admin mixin class providing a PriceGroup member field method."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import reverse
from django.utils.safestring import mark_safe

if TYPE_CHECKING:
  from items.models import PriceGroup


class PriceGroupMembersAdminMixin:
  """An admin mixin class providing a PriceGroup member field method."""

  def members(self, obj: PriceGroup | None) -> str:
    """Return an HTML representation of the price_group members."""
    html = '<ul style="margin-left: auto;">'
    if obj:
      for item in obj.items:
        html+='<li><a href="{}">{}</a></li>'.format(  # noqa: UP032
          reverse("admin:items_item_change", args=(item.pk,)),
          item.name_full,
        )
    html += "</ul>"
    return mark_safe(html)
