"""Test the admin for the Brand model."""

from items.admin.brand import BrandAdmin


class TestBrandAdmin:
  """Test the BrandAdmin class."""

  def test_instantiate__ordering(
      self,
      brand_admin: BrandAdmin,
  ) -> None:
    assert brand_admin.ordering == ('name',)
