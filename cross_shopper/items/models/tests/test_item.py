"""Test the Item model."""

from typing import Callable, List

import pytest
from items import constants
from items.models import Attribute, Item, Packaging


@pytest.mark.django_db
class TestItem:
  attribute_order_scenario = pytest.mark.parametrize(
      "attribute_count,summary_builder",
      (
          (0, lambda item: ""),
          (1, lambda item: "[{}]".format(str(item.attribute.all()[0]))),
          (
              2,
              lambda item: "[{}]".
              format(", ".join(map(str, item.attribute.order_by("name")))),
          ),
      ),
  )

  @pytest.mark.parametrize("non_gmo", [True, False])
  def test_clean__is_organic__always_sets_non_gmo_to_true(
      self,
      item: Item,
      non_gmo: bool,
  ) -> None:
    item.is_organic = True
    item.is_non_gmo = non_gmo

    item.save()

    assert item.is_non_gmo is True

  @attribute_order_scenario
  def test_attribute_summary__vary_sorted_attributes__returns_correct_summary(
      self,
      item: Item,
      attribute_alternate: Attribute,
      attribute_count: int,
      summary_builder: Callable[[Item], str],
  ) -> None:
    if attribute_count == 0:
      item.attribute.clear()
    if attribute_count == 2:
      item.attribute.add(attribute_alternate)

    assert item.attribute_summary == summary_builder(item)

  @attribute_order_scenario
  def test_attribute_summary__vary_unsorted_attributes__returns_correct_summary(
      self,
      item: Item,
      attribute_alternate: Attribute,
      attribute_count: int,
      summary_builder: Callable[[Item], str],
  ) -> None:
    if attribute_count == 0:
      item.attribute.clear()
    if attribute_count == 2:
      item.attribute.add(attribute_alternate)
    item.attribute.set(item.attribute.all().reverse())

    assert item.attribute_summary == summary_builder(item)

  def test_is_bulk__bulk_packaging__returns_false(
      self,
      item: Item,
      packaging_as_bulk: Packaging,
  ) -> None:
    item.packaging = packaging_as_bulk

    assert item.is_bulk is True

  def test_is_bulk__non_bulk_packaging__returns_false(
      self,
      item: Item,
      packaging_as_non_bulk: Packaging,
  ) -> None:
    item.packaging = packaging_as_non_bulk

    assert item.is_bulk is False

  @pytest.mark.parametrize(
      "has_attributes,name_builder",
      (
          (
              False,
              lambda item: item.name,
          ),
          (
              True,
              lambda item: " ".join([
                  item.name,
                  item.attribute_summary,
              ]),
          ),
      ),
  )
  def test_name_attributed__vary_attributes__returns_correct_name(
      self,
      item: Item,
      has_attributes: bool,
      name_builder: Callable[[Item], str],
  ) -> None:
    if not has_attributes:
      item.attribute.clear()

    assert item.name_attributed == name_builder(item)

  @pytest.mark.parametrize(
      "is_organic,has_attributes,name_builder",
      (
          (
              True,
              True,
              lambda item: [
                  " ".join(
                      [
                          constants.ITEM_NAME_PREFIX_ORGANIC,
                          item.name,
                          item.attribute_summary,
                      ]
                  ),
                  item.brand,
                  item.packaging,
              ],
          ),
          (
              False,
              True,
              lambda item: [
                  " ".join([
                      item.name,
                      item.attribute_summary,
                  ]),
                  item.brand,
                  item.packaging,
              ],
          ),
          (
              True,
              False,
              lambda item: [
                  " ".join([
                      constants.ITEM_NAME_PREFIX_ORGANIC,
                      item.name,
                  ]),
                  item.brand,
                  item.packaging,
              ],
          ),
          (
              False,
              False,
              lambda item: [
                  item.name,
                  item.brand,
                  item.packaging,
              ],
          ),
      ),
  )
  def test_name_full__vary_organic__vary_attributes_correct_name(
      self,
      item: Item,
      is_organic: bool,
      has_attributes: bool,
      name_builder: Callable[[Item], List[str]],
  ) -> None:
    item.is_organic = is_organic
    if not has_attributes:
      item.attribute.clear()

    assert item.name_full == ", ".join(map(str, name_builder(item)))

  def test_str__is_organic__returns_name_full(
      self,
      item: Item,
  ) -> None:
    item.is_organic = True

    assert str(item) == item.name_full

  def test_str__is_not_organic__returns_name_full(
      self,
      item: Item,
  ) -> None:
    item.is_organic = False

    assert str(item) == item.name_full
