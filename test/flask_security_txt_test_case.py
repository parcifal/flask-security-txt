"""
A base test case for the Flask-SecurityTxt extension.
"""

import re
from abc import ABC
from typing import Any, Optional
from unittest import TestCase

from flask import Flask

from flask_security_txt import SecurityTxt


class FlaskSecurityTxtTestCase(ABC, TestCase):
    """
    Base test case class for testing Flask applications integrated with
    SecurityTxt.

    This abstract class provides utility methods for verifying HTTP status
    codes and response lines in `.well-known/security.txt` endpoint responses.
    It is intended to be subclassed and used to write test cases for Flask
    applications that use the SecurityTxt library.
    """

    def setUp(self) -> None:
        self.app = Flask(__name__)

    # pylint: disable=invalid-name
    def assertHTTPStatus(self,
                         expected_status_code: int = 200,
                         request_uri: str = "/.well-known/security.txt",
                         constructor_kwargs: Optional[dict[str, Any]] = None,
                         app_config: Optional[dict[str, Any]] = None):
        """
        Assert that the specified request URI returns the expected http: status
        code.
        """
        if constructor_kwargs is None:
            constructor_kwargs = {}
        if app_config is not None:
            self.app.config.update(app_config)

        SecurityTxt(self.app, **constructor_kwargs)

        response = self.app.test_client().get(request_uri)
        self.assertEqual(expected_status_code, response.status_code)

    def assertLinesMatch(self,
                         request_uri: str = "/.well-known/security.txt",
                         constructor_kwargs: Optional[dict[str, Any]] = None,
                         app_config: Optional[dict[str, Any]] = None,
                         lines: Optional[list[str]] = None):
        """
        Assert that each entry in `lines` appears as a complete line somewhere
        in the response body.
        """
        if lines is None or len(lines) == 0:
            return

        if constructor_kwargs is None:
            constructor_kwargs = {}
        if app_config is not None:
            self.app.config.update(app_config)

        SecurityTxt(self.app, **constructor_kwargs)

        response = self.app.test_client().get(request_uri)
        response_lines = response.text.splitlines()

        for expected_line in lines:
            pattern = re.compile(f"^{re.escape(expected_line)}$")

            if any(pattern.match(line) for line in response_lines):
                continue

            raise self.failureException(
                f"Line \"{expected_line}\" not found in response.\n"
                f"Response body:\n{response.text}"
            )

    def assertLineAbsent(self,
                         request_uri: str = "/.well-known/security.txt",
                         constructor_kwargs: Optional[dict[str, Any]] = None,
                         app_config: Optional[dict[str, Any]] = None,
                         line_prefix: Optional[str] = None):
        """
        Assert that no line in the response body starts with the given prefix.
        Useful for confirming that an optional field is omitted entirely.
        """
        if line_prefix is None:
            return

        if constructor_kwargs is None:
            constructor_kwargs = {}
        if app_config is not None:
            self.app.config.update(app_config)

        SecurityTxt(self.app, **constructor_kwargs)

        response = self.app.test_client().get(request_uri)
        response_lines = response.text.splitlines()

        for line in response_lines:
            if not line.startswith(line_prefix):
                continue

            raise self.failureException(
                f"Unexpected line starting with \"{line_prefix}\" found "
                f"in response:\n  {line}"
            )
