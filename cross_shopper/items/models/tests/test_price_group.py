"""Test the PriceGroup model."""

from typing import TYPE_CHECKING

import pytest
from django.core.exceptions import ValidationError
from items.models import PackagingUnit
from items.models.price_group import (
    CONSTRAINT_NAMES,
    VALIDATION_ERRORS,
    PriceGroup,
)

if TYPE_CHECKING:  # no cover
  from items.models import Item


@pytest.mark.django_db
class TestPriceGroup:

  def test_constraint__unique_name(
      self,
      price_group: "PriceGroup",
  ) -> None:
    price_group2 = PriceGroup(
        name=price_group.name,
        quantity=price_group.quantity,
        unit=price_group.unit,
    )

    with pytest.raises(ValidationError) as exc:
      price_group2.save()

    assert str(exc.value) == str(
        {
            '__all__':
                [
                    'Constraint '
                    f'“{CONSTRAINT_NAMES["name"]}” '
                    'is violated.',
                ]
        }
    )

  def test_clean__comparison_unit_incompatible__raises_exception(
      self,
      item: "Item",
  ) -> None:
    assert item.price_group is not None
    incompatible_packaging_unit = PackagingUnit.objects.create(
        name="incompatible",
    )
    item.price_group.unit = incompatible_packaging_unit

    with pytest.raises(ValidationError) as exc:
      item.price_group.save()

    assert str(exc.value) == str(VALIDATION_ERRORS['invalid_unit'])

  def test_has_item__no_related_item__returns_false(
      self,
      price_group: "PriceGroup",
  ) -> None:
    assert price_group.has_item is False

  def test_has_item__with_related_item__returns_true(
      self,
      item: "Item",
  ) -> None:
    assert item.price_group is not None
    assert item.price_group.has_item is True

  def test_items__no_related_item___returns_empty_query_set(
      self,
      price_group: "PriceGroup",
  ) -> None:
    assert price_group.items.count() == 0

  def test_items__with_related_item__returns_set_of_items(
      self,
      item: "Item",
  ) -> None:
    assert item.price_group is not None
    assert list(item.price_group.items) == [item]

  def test_str__returns_group_name(
      self,
      price_group: "PriceGroup",
  ) -> None:
    assert str(price_group) == str(price_group.name)
