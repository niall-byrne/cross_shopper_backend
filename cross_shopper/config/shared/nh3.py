"""Configuration for django-nh3."""
from __future__ import annotations

from typing import Callable

AliasNh3AllowAttributesFilter = \
    Callable[[str, str, str], str | None] | None

# Which HTML values to restore after transformation
NH3_RESTORE_CONFIG: dict[str, str] = {"&amp;": "&"}

NH3_ALLOWED_ATTRIBUTES: dict[str, str] = {}

NH3_ALLOWED_ATTRIBUTES_FILTER: AliasNh3AllowAttributesFilter = None

NH3_CLEAN_CONTENT_TAGS: set[str] = set()

NH3_LINK_REL: str = ""

NH3_STRIP_COMMENTS: bool = False

NH3_ALLOWED_TAGS: set[str] = set()
