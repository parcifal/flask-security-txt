"""
Type definitions for Flask-SecurityTxt.
"""

from typing import Optional, Union

FlaskSecurityTxtConfig = Optional[dict]

Field = list[str]
FieldValue = Union[str, list[str]]
