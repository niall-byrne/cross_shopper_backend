"""A title case transforming BlondeCharField extension."""

from utilities.strings.title import TitleString
from .blonde import BlondeCharField


class TitleField(BlondeCharField):

  def transform(self, value: str) -> str:
    """Transform the field value into a new form."""
    value = TitleString(value).as_title()
    return super().transform(value)
