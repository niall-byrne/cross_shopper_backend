"""Test the DynamicSubClass class."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from utilities.testing.comparisons.is_subclass import DynamicSubClass

if TYPE_CHECKING:
  from .conftest import (
      AliasAttributes,
      AliasGenericClass,
      AliasGenericClassFactory,
  )


class TestDynamicSubClass:

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
      attributes: AliasAttributes,
      generic_class: AliasGenericClass,
      generic_class_factory: AliasGenericClassFactory,
  ) -> None:
    subclass = generic_class_factory(attributes)

    assert subclass == (
        DynamicSubClass(
            base=generic_class,
            attributes=attributes,
        )
    )

  @scenarios
  def test_instantiate__missing_attribute__raises_an_exception(
      self,
      attributes: AliasAttributes,
      generic_class: AliasGenericClass,
      generic_class_factory: AliasGenericClassFactory,
  ) -> None:
    wrong_attributes = dict(attributes)
    del wrong_attributes["attr1"]

    subclass = generic_class_factory(wrong_attributes)

    with pytest.raises(Exception) as exc:
      assert subclass == (
          DynamicSubClass(
              base=generic_class,
              attributes=attributes,
          )
      )

    assert str(exc.value) == "".join(
        [
            f"'{subclass}' -- ",
            DynamicSubClass.Messages.attribute_missing.format("attr1"),
        ],
    )

  @scenarios
  def test_instantiate__wrong_attribute__raises_an_exception(
      self,
      attributes: AliasAttributes,
      generic_class: AliasGenericClass,
      generic_class_factory: AliasGenericClassFactory,
  ) -> None:
    wrong_attributes = dict(attributes)
    wrong_attributes["attr1"] = "wrong value"

    subclass = generic_class_factory(wrong_attributes)

    with pytest.raises(Exception) as exc:
      assert subclass == (
          DynamicSubClass(
              base=generic_class,
              attributes=attributes,
          )
      )

    assert str(exc.value) == "".join(
        [
            f"'{subclass}' -- ",
            DynamicSubClass.Messages.attribute_wrong.format(
                "attr1",
                wrong_attributes["attr1"],
                attributes["attr1"],
            )
        ],
    )

  @scenarios
  def test_instantiate__not_a_class__raises_exception(
      self,
      attributes: AliasAttributes,
      generic_class: AliasGenericClass,
  ) -> None:

    with pytest.raises(Exception) as exc:
      assert 1 == (DynamicSubClass(
          base=generic_class,
          attributes=attributes,
      ))

    assert str(exc.value) == "'1' -- " + DynamicSubClass.Messages.not_a_class

  @scenarios
  def test_instantiate__not_a_subclass__raises_exception(
      self,
      attributes: AliasAttributes,
      generic_class: AliasGenericClass,
  ) -> None:

    class NonMatching:
      pass

    with pytest.raises(Exception) as exc:
      assert NonMatching == (
          DynamicSubClass(
              base=generic_class,
              attributes=attributes,
          )
      )

    assert str(exc.value) == "".join(
        [
            f"'{NonMatching}' -- ",
            DynamicSubClass.Messages.not_a_subclass.format(generic_class),
        ],
    )

  @scenarios
  def test_instantiate__repr__returns_expected_string(
      self,
      attributes: AliasAttributes,
      generic_class: AliasGenericClass,
  ) -> None:
    instance = DynamicSubClass(
        base=generic_class,
        attributes=attributes,
    )

    assert repr(instance) == str(instance.__class__)
