"""Represent a string as an entity title."""

import re


class TitleString(str):
  """A string that can be used as a title for an entity."""

  WHITELIST = {
      "a", "an", "the", "and", "but", "or", "for", "nor", "on", "at", "to",
      "from", "by", "with"
  }
  _WORD_PATTERN = re.compile(r"\b[\w']+\b")

  def as_title(self) -> "str":
    """Format the string as an entity title."""
    converted = self._WORD_PATTERN.sub(lambda m: self._replace_logic(m), self)
    converted = self._force_first_word(converted)
    return converted

  def _replace_logic(self, match: re.Match[str]) -> "str":
    word = match.group(0)

    if word.lower() in self.WHITELIST:
      return word

    return word[0].upper() + word[1:]

  def _force_first_word(
      self,
      text: str,
  ) -> "str":
    return self._WORD_PATTERN.sub(
        lambda match: match.group(0)[0].upper() + match.group(0)[1:],
        text,
        count=1
    )
