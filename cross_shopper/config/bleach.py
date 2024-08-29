"""Configuration for django-bleach."""

# Which HTML values to restore after transformation
BLEACH_RESTORE_CONFIG: dict[str, str] = {"&amp;": "&"}

# Which HTML tags are allowed
BLEACH_ALLOWED_TAGS: list[str] = []

# Which HTML attributes are allowed
BLEACH_ALLOWED_ATTRIBUTES: list[str] = []

# Which CSS properties are allowed in 'style' attributes (assuming
# style is an allowed attribute)
BLEACH_ALLOWED_STYLES: list[str] = []

# Strip unknown tags if True, replace with HTML escaped characters if
# False
BLEACH_STRIP_TAGS = True

# Strip comments, or leave them in.
BLEACH_STRIP_COMMENTS = False
