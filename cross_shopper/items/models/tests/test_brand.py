"""Test the Brand model."""

import pytest
from django.core.exceptions import ValidationError
from items.models.brand import CONSTRAINT_NAMES, Brand


@pytest.mark.django_db
class TestBrand:
  mocked_brand_name = "not_a_real_company"

  def test_name__is_unique(self,) -> None:
    brand = Brand(name=self.mocked_brand_name)
    brand.save()

    with pytest.raises(ValidationError) as exc:
      brand2 = Brand(name=self.mocked_brand_name)
      brand2.save()

    assert str(exc.value) == str(
        {
            "__all__":
                [
                    'Constraint '
                    f'“{CONSTRAINT_NAMES["name"]}” '
                    'is violated.',
                ]
        }
    )

  def test_str__returns_brand_name(self,) -> None:
    brand = Brand(name=self.mocked_brand_name)

    assert str(brand) == self.mocked_brand_name
