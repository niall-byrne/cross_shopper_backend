"""Configuration for django-bleach."""

from typing import Dict, List

# Which HTML values to restore after transformation
BLEACH_RESTORE_CONFIG: Dict[str, str] = {"&amp;": "&"}

# Which HTML tags are allowed
BLEACH_ALLOWED_TAGS: List[str] = []

# Which HTML attributes are allowed
BLEACH_ALLOWED_ATTRIBUTES: List[str] = []

# Which CSS properties are allowed in 'style' attributes (assuming
# style is an allowed attribute)
BLEACH_ALLOWED_STYLES: List[str] = []

# Strip unknown tags if True, replace with HTML escaped characters if
# False
BLEACH_STRIP_TAGS = True

# Strip comments, or leave them in.
BLEACH_STRIP_COMMENTS = False
