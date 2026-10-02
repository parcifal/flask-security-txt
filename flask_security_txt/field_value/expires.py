"""
Expires field value definition.
"""

from datetime import datetime as dt, timedelta as td, timezone as tz

from dateutil import parser
from dateutil.parser import ParserError
from flask import current_app

from flask_security_txt.lib import FieldValue


def get_expires_field_value() -> FieldValue:
    """
    @return:
        The value of the expires field.
    """
    value = current_app.config.get("SECURITY_TXT_EXPIRES")

    if isinstance(value, str):
        try:
            value = parser.parse(value)
        except ParserError as e:
            raise ValueError("SECURITY_TXT_EXPIRES string must use a"
                             "valid datetime format") from e
        except Exception as e:
            raise ValueError("SECURITY_TXT_EXPIRES could not be "
                             "parsed") from e
    if isinstance(value, dt):
        if value.tzinfo is None:
            # fall back to utc if no tz is available
            value = value.replace(tzinfo=tz.utc)

        return value.replace(microsecond=0).isoformat()

    if value is not None:
        raise ValueError("SECURITY_TXT_EXPIRES must be None, a string, "
                         "or a datetime")

    offset = current_app.config.get("SECURITY_TXT_EXPIRES_OFFSET")

    if isinstance(offset, td):
        pass
    elif isinstance(offset, tuple):
        offset = td(*offset)
    elif isinstance(offset, dict):
        try:
            offset = td(**offset)
        except TypeError as e:
            raise ValueError("SECURITY_TXT_EXPIRES_OFFSET dict must "
                             "contain valid timedelta arguments") from e
    else:
        raise ValueError("SECURITY_TXT_EXPIRES_OFFSET must be a timedelta, "
                         "tuple, or dict")

    value = dt.now(tz.utc) + offset
    return value.replace(microsecond=0).isoformat()
