"""Test the ItemAttribute model."""

import pytest
from django.core.exceptions import ValidationError
from items.models import ItemAttribute


@pytest.mark.django_db
class TestItemAttribute:

  def test_constraint__unique_together(
      self,
      item_attribute: ItemAttribute,
  ) -> None:
    item_attribute2 = ItemAttribute(
        item=item_attribute.item,
        attribute=item_attribute.attribute,
    )

    with pytest.raises(ValidationError) as exc:
      item_attribute2.save()

    assert str(exc.value) == str(
        {
            "__all__":
                ["Item attribute with this Item and Attribute already exists."],
        }
    )

  def test_str__returns_str_of_scraper_config(
      self,
      item_attribute: ItemAttribute,
  ) -> None:
    assert str(item_attribute
              ) == (f"{item_attribute.item.name} - {item_attribute.attribute}")
