"""Test the Item model."""

import pytest
from items.models import Item, Packaging


@pytest.mark.django_db
class TestItem:

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

  def test__is_bulk__bulk_packaging__returns_false(
      self,
      item: Item,
      packaging_as_bulk: Packaging,
  ) -> None:
    item.packaging = packaging_as_bulk

    assert item.is_bulk is True

  def test__is_bulk__non_bulk_packaging__returns_false(
      self,
      item: Item,
      packaging_as_non_bulk: Packaging,
  ) -> None:
    item.packaging = packaging_as_non_bulk

    assert item.is_bulk is False

  def test_full_name__is_organic__returns_correct_name(
      self,
      item: Item,
  ) -> None:
    item.is_organic = True

    assert item.full_name == ", ".join(
        map(
            str, [
                " ".join([item.NAME_PREFIX_ORGANIC, item.name]),
                item.brand,
                item.packaging,
            ]
        )
    )

  def test_full_name__is_not_organic__returns_correct_name(
      self,
      item: Item,
  ) -> None:
    item.is_organic = False

    assert item.full_name == ", ".join(
        map(str, [
            item.name,
            item.brand,
            item.packaging,
        ])
    )

  def test_str__is_organic__returns_full_name(
      self,
      item: Item,
  ) -> None:
    item.is_organic = True

    assert str(item) == item.full_name

  def test_str__is_not_organic__returns_full_name(
      self,
      item: Item,
  ) -> None:
    item.is_organic = False

    assert str(item) == item.full_name
