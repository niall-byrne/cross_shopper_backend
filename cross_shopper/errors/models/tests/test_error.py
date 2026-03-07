"""Test the Error model."""

import pytest
from django.core.exceptions import ValidationError
from errors.models import Error


@pytest.mark.django_db
class TestError:

  def test_constraint__unique_together(self, error: Error) -> None:
    error2 = Error(
        type=error.type,
        item=error.item,
        scraper_config=error.scraper_config,
        store=error.store,
        count=1,
    )

    with pytest.raises(ValidationError) as exc:
      error2.save()

    assert str(exc.value) == str(
        {
            "__all__":
                [
                    "Error with this Type, Item, Scraper config and Store already exists."
                ]
        }
    )

  def test_str__returns_correct_value(
      self,
      error: Error,
  ) -> None:
    assert str(error) == (
        f"{error.type}: {str(error.item.name_full)} - {error.store}"
    )
