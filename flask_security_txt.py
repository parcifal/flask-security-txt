"""
The Flask-SecurityTxt extension.
"""

from collections.abc import Iterable

from datetime import datetime as dt, timedelta as td
from flask import Flask, Response, request, url_for, current_app


# pylint: disable=too-few-public-methods
class SecurityTxt:
    """
    Extends Flask application with a dynamically generated security.txt.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, app: Flask = None,
                 default_endpoint: str = "security_txt",
                 default_contact_local_part: str = "security",
                 default_expires_offset: tuple = (0, 0, 0, 0, 0, 0, 1),
                 default_dir: str = ".well-known",
                 default_file_name: str = "security.txt"):
        self.app = app

        self._default_endpoint = default_endpoint
        self._default_contact_local_part = default_contact_local_part
        self._default_expires_offset = default_expires_offset
        self._default_dir = default_dir
        self._default_file_name = default_file_name

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """
        Initialize the specified Flask application to generate a security.txt.
        """
        if not hasattr(app, "extensions"):
            app.extensions = {}

        app.extensions["security_txt"] = self

        app.config.setdefault("SECURITY_TXT_ENDPOINT",
                              self._default_endpoint)
        app.config.setdefault("SECURITY_TXT_CONTACT_LOCAL_PART",
                              self._default_contact_local_part)
        app.config.setdefault("SECURITY_TXT_EXPIRES_OFFSET",
                              self._default_expires_offset)

        _dir = app.config.get("WELL_KNOWN_DIR",
                              self._default_dir)
        name = app.config.get("SECURITY_TXT_FILE_NAME",
                              self._default_file_name)

        app.add_url_rule("/" + _dir + "/" + name,
                         app.config.get("SECURITY_TXT_ENDPOINT"),
                         self._send_security_txt)

    def _send_security_txt(self):
        """
        @return:
            The full security.txt as an HTTP response.
        """
        body = []

        for key, item in self._get_fields().items():
            if item is None:
                continue

            if isinstance(item, str):
                item = [item]

            assert isinstance(item, Iterable)

            for value in item:
                body.append(f"{key}: {value}")

        return Response("\n".join(body), mimetype="text/plain")

    def _get_fields(self) -> dict:
        """
        @return:
            A dict mapping the keys to the values of the security.txt fields.
        """
        return {
            "Contact":
                self._get_field_value_contact(),
            "Expires":
                self._get_field_value_expires(),
            "Encryption":
                self._get_field_value_encryption(),
            "Acknowledgments":
                self._get_field_value_acknowledgements(),
            "Preferred-Languages":
                self._get_field_value_preferred_languages(),
            "Canonical":
                self._get_field_value_canonical(),
            "Policy":
                self._get_field_value_policy(),
            "Hiring":
                self._get_field_value_hiring()
        }

    def _get_field_value_contact(self) -> str:
        """
        @return:
            The value of the contact field.
        """
        value = current_app.config.get("SECURITY_TXT_CONTACT")

        if value is not None:
            assert isinstance(value, (str, list, tuple))
            return value

        value = current_app.config.get("SECURITY_TXT_CONTACT_LOCAL_PART")

        assert isinstance(value, str)

        domain = request.host.rsplit(":", 1)[0]

        return f"mailto:{value}@{domain}"

    def _get_field_value_expires(self) -> str:
        """
        @return:
            The value of the expires field.
        """
        value = current_app.config.get("SECURITY_TXT_EXPIRES")

        if isinstance(value, str):
            return value
        if isinstance(value, dt):
            return value.isoformat()

        assert value is None

        offset = current_app.config.get("SECURITY_TXT_EXPIRES_OFFSET")

        if isinstance(offset, td):
            value = dt.now() + offset
        if isinstance(offset, tuple):
            value = dt.now() + td(*offset)

        assert isinstance(value, dt)
        return value.isoformat()

    def _get_field_value_encryption(self):
        """
        @return:
            The value of the encryption field.
        """
        return current_app.config.get("SECURITY_TXT_ENCRYPTION")

    def _get_field_value_acknowledgements(self):
        """
        @return:
            The value of the acknowledgements field.
        """
        return current_app.config.get("SECURITY_TXT_ACKNOWLEDGMENTS")

    def _get_field_value_preferred_languages(self):
        """
        @return:
            The value of the preferred languages field.
        """
        value = current_app.config.get("SECURITY_TXT_PREFERRED_LANGUAGES")

        if isinstance(value, str):
            return value
        if isinstance(value, (list, tuple)):
            return ", ".join(value)
        if not hasattr(current_app, "babel_instance"):
            return ""

        babel = getattr(current_app, "babel_instance")

        return ", ".join([
            t.language for t in getattr(babel, "list_translations")()
        ])

    def _get_field_value_canonical(self):
        """
        @return:
            The value of the canonical field.
        """
        value = current_app.config.get("SECURITY_TXT_CANONICAL")

        if value is not None:
            assert isinstance(value, str)
            return value

        endpoint = current_app.config.get("SECURITY_TXT_ENDPOINT")

        return f"https://{request.host}" + url_for(endpoint)

    def _get_field_value_policy(self):
        """
        @return:
            The value of the policy field.
        """
        return current_app.config.get("SECURITY_TXT_POLICY")

    def _get_field_value_hiring(self):
        """
        @return:
            The value of the hiring field.
        """
        return current_app.config.get("SECURITY_TXT_HIRING")
