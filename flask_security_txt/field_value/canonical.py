"""
Canonical field value definition.
"""

from flask import current_app

from flask_security_txt.lib import FieldValue
from flask_security_txt.util import list_urls_from_value


def get_canonical_field_value() -> FieldValue:
    """
    @return:
        The value of the canonical field.
    """
    canonical = current_app.config.get("SECURITY_TXT_CANONICAL")

    if not canonical:
        canonical = current_app.config.get("SECURITY_TXT_ENDPOINT")

    try:
        return list_urls_from_value(canonical)
    except ValueError as e:
        raise ValueError(
            "SECURITY_TXT_CANONICAL or SECURITY_TXT_ENDPOINT is "
            "misconfigured"
        ) from e
