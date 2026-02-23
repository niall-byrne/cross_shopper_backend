"""Test the InstanceOfClass class."""

from typing import TYPE_CHECKING

import pytest
from utilities.testing.comparisons.instance import InstanceOfClass

if TYPE_CHECKING:  # no cover
  from .conftest import (
      AliasAttributes,
      AliasGenericClass,
  )


class TestInstanceOfClass:

  scenarios = pytest.mark.parametrize(
      "attributes",
      (
          {
              "attr1": True,
              "attr2": "string",
              "attr3": 1
          },
          {
              "attr1": False,
              "attr2": "string2",
              "attr3": 2
          },
      ),
  )

  @scenarios
  def test_instantiate__correct_attributes__evaluates_as_equal(
      self,
      attributes: "AliasAttributes",
      generic_class: "AliasGenericClass",
  ) -> None:
    instance = generic_class(attributes)

    assert instance == InstanceOfClass(
        base=generic_class,
        attributes=attributes,
    )

  @scenarios
  def test_instantiate__missing_attribute__raises_an_exception(
      self,
      attributes: "AliasAttributes",
      generic_class: "AliasGenericClass",
  ) -> None:
    wrong_attributes = dict(attributes)
    del wrong_attributes["attr1"]

    instance = generic_class(wrong_attributes)

    with pytest.raises(Exception) as exc:
      assert instance == InstanceOfClass(
          base=generic_class,
          attributes=attributes,
      )

    assert str(exc.value) == "".join(
        [
            f"'{instance}' -- ",
            InstanceOfClass.Messages.attribute_missing.format("attr1"),
        ],
    )

  @scenarios
  def test_instantiate__not_a_class__raises_exception(
      self,
      attributes: "AliasAttributes",
      generic_class: "AliasGenericClass",
  ) -> None:

    with pytest.raises(Exception) as exc:
      assert 1 == InstanceOfClass(
          base=generic_class,
          attributes=attributes,
      )

    assert str(exc.value) == (
        "'1' -- " +
        InstanceOfClass.Messages.not_an_instance.format(generic_class)
    )

  @scenarios
  def test_instantiate__wrong_attribute__raises_an_exception(
      self,
      attributes: "AliasAttributes",
      generic_class: "AliasGenericClass",
  ) -> None:
    wrong_attributes = dict(attributes)
    wrong_attributes["attr1"] = "wrong value"

    instance = generic_class(wrong_attributes)

    with pytest.raises(Exception) as exc:
      assert instance == InstanceOfClass(
          base=generic_class,
          attributes=attributes,
      )

    assert str(exc.value) == "".join(
        [
            f"'{instance}' -- ",
            InstanceOfClass.Messages.attribute_wrong.format(
                "attr1",
                wrong_attributes["attr1"],
                attributes["attr1"],
            )
        ],
    )

  @scenarios
  def test_instantiate__repr__returns_expected_string(
      self,
      attributes: "AliasAttributes",
      generic_class: "AliasGenericClass",
  ) -> None:
    instance = InstanceOfClass(
        base=generic_class,
        attributes=attributes,
    )

    assert repr(instance) == str(instance.__class__)
