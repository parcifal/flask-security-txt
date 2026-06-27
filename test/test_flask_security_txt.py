"""
A test case for the Flask-SecurityTxt extension.
"""
import re
from datetime import datetime as dt, timedelta as td, timezone as tz
from typing import Any, Optional
from unittest import TestCase

from flask import Flask

from flask_security_txt import SecurityTxt


class TestFlaskSecurityTxt(TestCase):
    """
    Test the view end-points of the Flask app. Verify correct functionality by
    asserting that each known end-point has a response with an HTTP response
    code of 200, and that the response body contains the expected field lines.

    Note: constructor kwargs (e.g. default_endpoint) are passed via the
    `constructor_kwargs` parameter, while Flask app.config keys (e.g.
    SECURITY_TXT_CONTACT) are passed via the `app_config` parameter.
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
        Assert that the specified request URI returns HTTP 200.
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

        Note: the original implementation used re.match() against the full
        response text, which only matches at the very start of the string and
        will never find a line in the middle of the body. This version splits
        the response into individual lines and matches each one exactly.
        """
        if not lines:
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
            if not any(pattern.match(actual_line) for actual_line in
                       response_lines):
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

        for actual_line in response_lines:
            if actual_line.startswith(line_prefix):
                raise self.failureException(
                    f"Unexpected line starting with \"{line_prefix}\" found "
                    f"in response:\n  {actual_line}"
                )

    def test_security_txt_default(self):
        """Default path /.well-known/security.txt returns 200."""
        self.assertHTTPStatus(
            request_uri="/.well-known/security.txt"
        )

    def test_security_txt_endpoint_invalid(self):
        """
        Assert that the security.txt is still served as expected
        with a custom endpoint.
        """
        self.assertHTTPStatus(app_config={
            "SECURITY_TXT_ENDPOINT": "spam"
        })

    def test_security_txt_custom_dir(self):
        """
        Assert that the security.txt is served as expected
        at a custom well-known dir.
        """
        self.assertHTTPStatus(
            request_uri="/spam/security.txt",
            app_config={
                "WELL_KNOWN_DIR": "spam"
            }
        )

    def test_security_txt_custom_file_name(self):
        """
        Assert that the security.txt is served as expected
        with a custom file-name.
        """
        self.assertHTTPStatus(
            request_uri="/.well-known/spam.txt",
            app_config={
                "SECURITY_TXT_FILE_NAME": "spam.txt"
            }
        )

    def test_config_contact_default(self):
        """
        Assert that the default mailbox is rendered as expected.
        """
        self.assertLinesMatch(lines=[
            "Contact: mailto:security@localhost"
        ])

    def test_config_contact_mailbox(self):
        """
        Assert that a custom mailbox is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_CONTACT_MAILBOX": "spam"
            },
            lines=[
                "Contact: mailto:spam@localhost"
            ]
        )

    def test_config_contact_mailto(self):
        """
        Assert that a custom mailto contact is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_CONTACT": "mailto:spam@bacon.eggs"
            },
            lines=[
                "Contact: mailto:spam@bacon.eggs"
            ]
        )

    def test_config_contact_https(self):
        """
        Assert that a custom https contact is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_CONTACT": "https://spam.eggs/bacon"
            },
            lines=[
                "Contact: https://spam.eggs/bacon"
            ]
        )

    def test_config_contact_tel(self):
        """
        Assert that a custom tel contact is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_CONTACT": "tel:+31612345678"
            },
            lines=[
                "Contact: tel:+31612345678"
            ]
        )

    def test_config_contact_multiple(self):
        """
        Assert that multiple contacts are rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_CONTACT": [
                    "mailto:spam@bacon.eggs",
                    "https://bacon.eggs/spam",
                    "tel:+31612345678"
                ]
            },
            lines=[
                "Contact: mailto:spam@bacon.eggs",
                "Contact: https://bacon.eggs/spam",
                "Contact: tel:+31612345678"
            ]
        )

    def test_config_contact_http(self):
        """
        Assert that a custom http contact is not accepted.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_CONTACT": "http://spam.eggs/bacon"
            }
        )

    def test_config_contact_no_scheme(self):
        """
        Assert that a contact without scheme is not accepted.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_CONTACT": "spam"
            }
        )

    def test_config_expires_offset_timedelta(self):
        """
        Assert that an expires offset timedelta is accepted.
        """
        self.assertHTTPStatus(
            app_config={
                "SECURITY_TXT_EXPIRES_OFFSET": td(days=180)
            }
        )

    def test_config_expires_offset_tuple(self):
        """
        Assert that an expires offset tuple is accepted.
        """
        self.assertHTTPStatus(
            app_config={
                "SECURITY_TXT_EXPIRES_OFFSET": (0, 0, 90)
            }
        )

    def test_config_expires_datetime(self):
        """
        Assert that an expires datetime is rendered as expected.
        """
        expires = dt(2026, 12, 31, 23, 59, 59, tzinfo=tz.utc)
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_EXPIRES": expires
            },
            lines=[
                "Expires: 2026-12-31T23:59:59+00:00"
            ]
        )

    def test_config_expires_string(self):
        """
        Assert that an expires string is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_EXPIRES": "2026-12-31T23:59:59+00:00"
            },
            lines=[
                "Expires: 2026-12-31T23:59:59+00:00"
            ]
        )

    def test_config_expires_ms_stripped(self):
        """
        Assert that an expires datetime with microseconds
        is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_EXPIRES": dt(
                    2026,
                    12,
                    31,
                    23,
                    59,
                    59,
                    123456,
                    tz.utc
                )
            },
            lines=[
                "Expires: 2026-12-31T23:59:59+00:00"
            ]
        )

    def test_config_expires_invalid(self):
        """
        Assert that an invalid expires value is not accepted.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_EXPIRES": "spam"
            }
        )

    def test_config_expires_offset_invalid(self):
        """
        Assert that an invalid expires offset is not accepted.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_EXPIRES_OFFSET": "spam"
            }
        )

    def test_config_encryption_default(self):
        """
        Assert that no encryption URLs are rendered by default.
        """
        self.assertLineAbsent(line_prefix="Encryption:")

    def test_config_encryption_https(self):
        """
        Assert that an encryption https URL is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_ENCRYPTION": "https://spam.eggs/bacon"
            },
            lines=[
                "Encryption: https://spam.eggs/bacon"
            ]
        )

    def test_config_encryption_openpgp4fpr(self):
        """
        Assert that an encryption openpgp4fpr URL is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_ENCRYPTION": "openpgp4fpr:5F2DE5521600DEFA"
            },
            lines=[
                f"Encryption: openpgp4fpr:5F2DE5521600DEFA"
            ]
        )

    def test_config_acknowledgments_default(self):
        """
        Assert that no acknowledgments are rendered by default.
        """
        self.assertLineAbsent(line_prefix="Acknowledgments:")

    def test_config_acknowledgments_https(self):
        """
        Assert that an acknowledgments https URL is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_ACKNOWLEDGEMENTS": "https://spam.eggs/bacon"
            },
            lines=[
                "Acknowledgments: https://spam.eggs/bacon"
            ]
        )

    def test_config_acknowledgments_http_invalid(self):
        """
        Assert that an acknowledgments https URL is rendered as expected.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_ACKNOWLEDGEMENTS": "http://spam.eggs/bacon"
            }
        )

    def test_config_preferred_languages_default(self):
        """
        Assert that the preferred language is en by default.
        """
        self.assertLinesMatch(lines=[
            "Preferred-Languages: en"
        ])

    def test_config_preferred_languages_string(self):
        """
        Assert that a string of preferred languages is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_PREFERRED_LANGUAGES": "nl, en"
            },
            lines=[
                "Preferred-Languages: nl, en"
            ]
        )

    def test_config_preferred_languages_tuple(self):
        """
        Assert that a tuple of preferred languages is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_PREFERRED_LANGUAGES": ("nl", "en")
            },
            lines=[
                "Preferred-Languages: nl, en"
            ]
        )

    def test_config_preferred_languages_list(self):
        """
        Assert that a list of preferred languages is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_PREFERRED_LANGUAGES": ["nl", "en"]
            },
            lines=[
                "Preferred-Languages: nl, en"
            ]
        )

    def test_config_canonical_https(self):
        """
        Assert that a canonical URL is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_CANONICAL": "https://spam.eggs/bacon"
            },
            lines=[
                "Canonical: https://spam.eggs/bacon"
            ]
        )

    def test_config_canonical_http_invalid(self):
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_CANONICAL": "http://spam.eggs/bacon"
            }
        )

    def test_config_canonical_scheme_invalid(self):
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_CANONICAL": "ham://spam.eggs/bacon"
            }
        )

    def test_config_canonical_scheme_absent(self):
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_CANONICAL": "spam"
            }
        )

    def test_config_policy_default(self):
        """
        Assert that a policy line is absent by default.
        """
        self.assertLineAbsent(line_prefix="Policy:")

    def test_config_policy_https(self):
        """
        Assert that a policy https URL is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_POLICY": "https://spam.eggs/bacon"
            },
            lines=[
                "Policy: https://spam.eggs/bacon"
            ]
        )

    def test_config_policy_http(self):
        """
        Assert that a policy http URL is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_POLICY": "http://spam.eggs/bacon"
            }
        )

    def test_config_policy_scheme_invalid(self):
        """
        Assert that a policy URL with a wrong scheme is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_POLICY": "ham://spam.eggs/bacon"
            }
        )

    def test_config_policy_scheme_absent(self):
        """
        Assert that a policy URL with an absent scheme is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_POLICY": "spam"
            }
        )

    def test_config_hiring_default(self):
        """
        Assert that hiring is not rendered by default.
        """
        self.assertLineAbsent(line_prefix="Hiring:")

    def test_config_hiring_https(self):
        """
        Assert that a hiring https URL is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_HIRING": "https://spam.eggs/bacon"
            },
            lines=[
                "Hiring: https://spam.eggs/bacon"
            ]
        )

    def test_config_hiring_http_invalid(self):
        """
        Assert that a hiring http URL is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_HIRING": "http://spam.eggs/bacon"
            }
        )

    def test_config_hiring_scheme_invalid(self):
        """
        Assert that a hiring non-https scheme URL is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_HIRING": "ham://spam.eggs/bacon"
            }
        )

    def test_config_hiring_value_invalid(self):
        """
        Assert that a hiring value without scheme is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_HIRING": "spam"
            }
        )

    def test_config_field_case_default(self):
        """
        Assert that field have the standard case by default.
        """
        self.assertLinesMatch(lines=["Contact: mailto:security@localhost"])

    def test_config_field_case_standard(self):
        """
        Assert that standard cased fields are rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_FIELD_CASE": "standard"
            },
            lines=[
                "Contact: mailto:security@localhost"
            ]
        )

    def test_config_field_case_lower(self):
        """
        Assert that lower-cased fields are rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_FIELD_CASE": "lower"
            },
            lines=[
                "contact: mailto:security@localhost"
            ]
        )

    def test_config_field_case_upper(self):
        """
        Assert that upper-cased fields are rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_FIELD_CASE": "upper"
            },
            lines=[
                "CONTACT: mailto:security@localhost"
            ]
        )
