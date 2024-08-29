"""Test the Store model."""

import pytest
from django.core.exceptions import ValidationError
from stores.models import Store


@pytest.mark.django_db
class TestStore:

  def test_constraint__unique_together(self, store: Store) -> None:
    store2 = Store(
        address=store.address,
        franchise=store.franchise,
        franchise_location=store.franchise_location,
    )

    with pytest.raises(ValidationError) as exc:
      store2.save()

    assert str(exc.value) == str(
        {
            '__all__':
                [
                    'Store with this Franchise and Franchise location '
                    'already exists.'
                ]
        }
    )

  def test_str__returns_franchise_name(self, store: Store) -> None:
    assert str(store) == f"{str(store.franchise.name)}: {str(store.address)}"
