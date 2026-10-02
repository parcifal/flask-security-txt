"""
Contact field value definition.
"""

from urllib.parse import urlsplit

from flask import current_app, request

from flask_security_txt.lib import FieldValue
from flask_security_txt.util import list_urls_from_value


def get_contact_field_value() -> FieldValue:
    """
    @return:
        The value of the contact field.
    """
    value = current_app.config.get("SECURITY_TXT_CONTACT")

    if not value:
        mailbox = current_app.config.get("SECURITY_TXT_CONTACT_MAILBOX")
        if not isinstance(mailbox, str):
            raise ValueError("SECURITY_TXT_CONTACT_MAILBOX must be "
                             "a string")
        host = current_app.config.get("SERVER_NAME") or request.host
        domain = urlsplit(f"//{host}").hostname
        return [f"mailto:{mailbox}@{domain}"]

    try:
        return list_urls_from_value(value, [
            "https", "mailto", "tel"])
    except ValueError as e:
        raise ValueError(
            "SECURITY_TXT_CONTACT is misconfigured") from e
