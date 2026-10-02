"""
Preferred languages field value definition.
"""

from flask import current_app

from flask_security_txt.lib import FieldValue

try:
    from flask_babel import get_babel
except ImportError:
    get_babel = None


def get_preferred_languages_field_value() -> FieldValue:
    """
    @return:
        The value of the preferred languages field.
    """
    value = current_app.config.get("SECURITY_TXT_PREFERRED_LANGUAGES")

    if value:
        if isinstance(value, str):
            return value
        if isinstance(value, (list, tuple)):
            return ", ".join(value)

    # fall back to babel if it is loaded, otherwise use default
    if get_babel and "babel" in current_app.extensions:
        babel = get_babel()
        tt = babel.instance.list_translations()

        if tt:
            return ", ".join([str(t).replace("_", "-") for t in tt])

    return "en"
