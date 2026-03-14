"""Test the PriceGroupMembersAdminMixin model."""

from typing import TYPE_CHECKING

import pytest
from items.admin.mixins.price_group_members import PriceGroupMembersAdminMixin

if TYPE_CHECKING:  # no cover
  from items.models import Item, PriceGroup


@pytest.mark.django_db
class TestPriceGroupMembersAdminMixin:

  def test_members__with_none__returns_correct_html(
      self,
      price_group_members_admin: PriceGroupMembersAdminMixin,
  ) -> None:
    html = price_group_members_admin.members(None)

    assert html == '<ul style="margin-left: auto;"></ul>'

  def test_members__with_an_empty_price_group__returns_correct_html(
      self,
      price_group: "PriceGroup",
      price_group_members_admin: PriceGroupMembersAdminMixin,
  ) -> None:
    html = price_group_members_admin.members(price_group)

    assert html == '<ul style="margin-left: auto;"></ul>'

  def test_members__with_1_member_price_group__returns_correct_html(
      self,
      item: "Item",
      price_group_members_admin: PriceGroupMembersAdminMixin,
  ) -> None:
    html = price_group_members_admin.members(item.price_group)

    assert html == (
        '<ul style="margin-left: auto;">'
        f'<li><a href="/admin/items/item/{item.pk}/change/">'
        f"{item.name_full}</a></li>"
        "</ul>"
    )

  def test_members__with_two_member_price_group__returns_correct_html(
      self,
      item: "Item",
      item_alternate: "Item",
      price_group_members_admin: PriceGroupMembersAdminMixin,
  ) -> None:
    item_alternate.price_group = item.price_group
    item_alternate.is_non_gmo = item.is_non_gmo
    item_alternate.is_organic = item.is_organic
    item_alternate.packaging.unit = item.packaging.unit
    item_alternate.packaging.save()
    item_alternate.save()

    html = price_group_members_admin.members(item.price_group)

    assert html == (
        '<ul style="margin-left: auto;">'
        f'<li><a href="/admin/items/item/{item.pk}/change/">'
        f"{item.name_full}</a></li>"
        f'<li><a href="/admin/items/item/{item_alternate.pk}/change/">'
        f"{item_alternate.name_full}</a></li>"
        "</ul>"
    )
