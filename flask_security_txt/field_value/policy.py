"""
Policy field value definition.
"""

from flask import current_app

from flask_security_txt.lib import FieldValue
from flask_security_txt.util import list_urls_from_value


def get_policy_field_value() -> FieldValue:
    """
    @return:
        The value of the policy field.
    """
    try:
        return list_urls_from_value(
            current_app.config.get("SECURITY_TXT_POLICY"))
    except ValueError as e:
        raise ValueError(
            "SECURITY_TXT_POLICY is misconfigured") from e
