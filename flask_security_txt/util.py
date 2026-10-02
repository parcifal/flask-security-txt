"""
Utility functions for Flask-SecurityTxt.
"""

import os
from typing import Union, Optional, Generator
from urllib.parse import urlsplit

from flask import current_app, url_for
from werkzeug.routing import BuildError


def list_urls_from_value(
        value: Union[str, list[str], None],
        schemes: Optional[list[str]] = None
) -> list[str]:
    """
    Parse zero or more URLs from the specified config value. The URLs can
    be defined as either a full URL string starting with one of the
    specified schemes or as an end-point that can be resolved by the
    Flask application.
    """
    if not value:
        return []
    if schemes is None:
        schemes = ["https"]
    if not schemes:
        return []
    if isinstance(value, str):
        value = [value]

    def yield_urls(vv: list[str], ss: list[str]) -> Generator[str, None, None]:
        for v in vv:
            url = urlsplit(v)

            if url.scheme in ss:
                yield v
                continue

            if current_app.has_static_folder and os.path.exists(
                    os.path.join(str(current_app.static_folder), v)):
                yield url_for("static",
                              filename=v,
                              _external=True,
                              _scheme="https")
                continue

            try:
                yield url_for(v, _external=True, _scheme="https")
            except BuildError as e:
                raise ValueError(
                    "A URL field value must either be string starting with "
                    "https://, the name of a static file or an end-point "
                    "name that can be resolved by the flask application"
                ) from e

    return list(yield_urls(value, schemes))
