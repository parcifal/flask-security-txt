"""
Hiring field value definition.
"""

from flask import current_app

from flask_security_txt.lib import FieldValue
from flask_security_txt.util import list_urls_from_value


def get_hiring_field_value() -> FieldValue:
    """
    @return:
        The value of the hiring field.
    """
    try:
        return list_urls_from_value(
            current_app.config.get("SECURITY_TXT_HIRING"))
    except ValueError as e:
        raise ValueError(
            "SECURITY_TXT_HIRING is misconfigured") from e
