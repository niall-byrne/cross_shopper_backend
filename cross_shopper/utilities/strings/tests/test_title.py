"""Tests for the TitleString class."""

from utilities.strings.title import TitleString
from .scenarios import title_string_scenarios


class TestTitleString:

  @title_string_scenarios
  def test_as_title__returns_expected_value(
      self,
      input_string: str,
      expected_string: str,
  ) -> None:
    title_string = TitleString(input_string)

    assert title_string.as_title() == expected_string
