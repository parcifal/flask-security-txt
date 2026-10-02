"""
Acknowledgments field value definition.
"""

from flask import current_app

from flask_security_txt.lib import FieldValue
from flask_security_txt.util import list_urls_from_value


def get_acknowledgments_field_value() -> FieldValue:
    """
    @return:
        The value of the acknowledgments field.
    """
    try:
        return list_urls_from_value(
            current_app.config.get("SECURITY_TXT_ACKNOWLEDGMENTS"))
    except ValueError as e:
        raise ValueError(
            "SECURITY_TXT_ACKNOWLEDGMENTS is misconfigured") from e
