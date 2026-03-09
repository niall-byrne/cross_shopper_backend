"""Configuration for django-nh3."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # no cover
  from typing import Callable, Dict, Optional, Set
  AliasNh3AllowAttributesFilter = \
    Optional[Callable[[str, str, str], Optional[str]]]

# Which HTML values to restore after transformation
NH3_RESTORE_CONFIG: "Dict[str, str]" = {'&amp;': '&'}

NH3_ALLOWED_ATTRIBUTES: "Dict[str, str]" = {}

NH3_ALLOWED_ATTRIBUTES_FILTER: "AliasNh3AllowAttributesFilter" = None

NH3_CLEAN_CONTENT_TAGS: "Set[str]" = set()

NH3_LINK_REL: "str" = ""

NH3_STRIP_COMMENTS: "bool" = False

NH3_ALLOWED_TAGS: "Set[str]" = set()
