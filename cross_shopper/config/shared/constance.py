"""Configuration for django-constance."""

CONSTANCE_CONFIG = {
    "ADMIN_AUTO_ATTACH_ITEMS_TO_REPORTS":
        (
            True,
            "Automatically attach edited items to all non-testing reports.",
        ),
}

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
