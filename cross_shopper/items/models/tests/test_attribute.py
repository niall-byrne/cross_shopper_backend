"""Test the Attribute model."""

from typing import TYPE_CHECKING

import pytest
from django.core.exceptions import ValidationError
from items.models.attribute import CONSTRAINT_NAMES, Attribute
from utilities.models.validators.restricted_values import VALIDATION_ERROR

if TYPE_CHECKING:  # no cover
  from items.models import ItemAttribute


@pytest.mark.django_db
class TestAttribute:

  def test_constraint__unique_name(
      self,
      attribute: "Attribute",
  ) -> None:
    attribute2 = Attribute(name=attribute.name)

    with pytest.raises(ValidationError) as exc:
      attribute2.save()

    assert str(exc.value) == str(
        {"__all__": [f"Constraint “{CONSTRAINT_NAMES['name']}” is violated.",]}
    )

  def test_has_item__no_related_item__returns_false(
      self,
      attribute: "Attribute",
  ) -> None:
    assert attribute.has_item is False

  def test_has_item__with_related_item__returns_true(
      self,
      item_attribute: "ItemAttribute",
  ) -> None:
    assert item_attribute.attribute.has_item is True

  def test_validation__commas_in_name__raises_exception(self) -> None:
    attribute = Attribute(name="invalid,attribute")

    with pytest.raises(ValidationError) as exc:
      attribute.save()

    assert str(exc.value) == str({"name": [VALIDATION_ERROR % ","]})

  def test_str__returns_attribute_name(
      self,
      attribute: "Attribute",
  ) -> None:
    assert str(attribute) == str(attribute.name)
