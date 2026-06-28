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
    asserting that each known end-point has a response with an http: response
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
        Assert that the specified request URI returns the expected http: status code.
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

    def test_security_txt_default(self):
        """
        Assert that the security.txt is served as expected at the default path.
        """
        self.assertHTTPStatus(
            request_uri="/.well-known/security.txt"
        )

    def test_security_txt_endpoint_custom(self):
        """
        Assert that the security.txt is served as expected
        with a custom endpoint name.
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
        with a custom file name.
        """
        self.assertHTTPStatus(
            request_uri="/.well-known/spam.txt",
            app_config={
                "SECURITY_TXT_FILE_NAME": "spam.txt"
            }
        )

    def test_config_contact_default(self):
        """
        Assert that the Contact field is rendered as expected by default.
        """
        self.assertLinesMatch(lines=[
            "Contact: mailto:security@localhost"
        ])

    def test_config_contact_mailbox(self):
        """
        Assert that a custom SECURITY_TXT_CONTACT_MAILBOX
        is rendered as expected.
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
        Assert that a mailto: Contact value is rendered as expected.
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
        Assert that an https: Contact value is rendered as expected.
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
        Assert that a tel: Contact value is rendered as expected.
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
        Assert that multiple Contact values are rendered as expected.
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
        Assert that an http: Contact value is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_CONTACT": "http://spam.eggs/bacon"
            }
        )

    def test_config_contact_scheme_absent(self):
        """
        Assert that a Contact value without a scheme is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_CONTACT": "spam"
            }
        )

    def test_config_expires_offset_timedelta(self):
        """
        Assert that a timedelta SECURITY_TXT_EXPIRES_OFFSET is accepted.
        """
        self.assertHTTPStatus(
            app_config={
                "SECURITY_TXT_EXPIRES_OFFSET": td(days=180)
            }
        )

    def test_config_expires_offset_tuple(self):
        """
        Assert that a tuple SECURITY_TXT_EXPIRES_OFFSET is accepted.
        """
        self.assertHTTPStatus(
            app_config={
                "SECURITY_TXT_EXPIRES_OFFSET": (0, 0, 90)
            }
        )

    def test_config_expires_datetime(self):
        """
        Assert that a datetime SECURITY_TXT_EXPIRES value is rendered
        as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_EXPIRES": dt(2026, 12, 31, 23, 59, 59, tzinfo=tz.utc)
            },
            lines=[
                "Expires: 2026-12-31T23:59:59+00:00"
            ]
        )

    def test_config_expires_string(self):
        """
        Assert that a string SECURITY_TXT_EXPIRES value
        is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_EXPIRES": "2026-12-31T23:59:59+00:00"
            },
            lines=[
                "Expires: 2026-12-31T23:59:59+00:00"
            ]
        )

    def test_config_expires_microseconds_stripped(self):
        """
        Assert that microseconds are stripped from a datetime
        SECURITY_TXT_EXPIRES value.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_EXPIRES": dt(2026, 12, 31, 23, 59, 59, 123456, tz.utc)
            },
            lines=[
                "Expires: 2026-12-31T23:59:59+00:00"
            ]
        )

    def test_config_expires_invalid(self):
        """
        Assert that an invalid SECURITY_TXT_EXPIRES value is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_EXPIRES": "spam"
            }
        )

    def test_config_expires_offset_invalid(self):
        """
        Assert that an invalid SECURITY_TXT_EXPIRES_OFFSET value is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_EXPIRES_OFFSET": "spam"
            }
        )

    def test_config_encryption_default(self):
        """
        Assert that no Encryption line is rendered by default.
        """
        self.assertLineAbsent(line_prefix="Encryption:")

    def test_config_encryption_https(self):
        """
        Assert that an https: Encryption value is rendered as expected.
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
        Assert that an openpgp4fpr: Encryption value is rendered as expected.
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
        Assert that no Acknowledgments line is rendered by default.
        """
        self.assertLineAbsent(line_prefix="Acknowledgments:")

    def test_config_acknowledgments_https(self):
        """
        Assert that an https: Acknowledgments value is rendered as expected.
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
        Assert that an http: Acknowledgments value is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_ACKNOWLEDGEMENTS": "http://spam.eggs/bacon"
            }
        )

    def test_config_preferred_languages_default(self):
        """
        Assert that the Preferred-Languages field is rendered
        as expected by default.
        """
        self.assertLinesMatch(lines=[
            "Preferred-Languages: en"
        ])

    def test_config_preferred_languages_string(self):
        """
        Assert that a string SECURITY_TXT_PREFERRED_LANGUAGES value
        is rendered as expected.
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
        Assert that a tuple SECURITY_TXT_PREFERRED_LANGUAGES value
        is rendered as expected.
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
        Assert that a list SECURITY_TXT_PREFERRED_LANGUAGES value
        is rendered as expected.
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
        Assert that an https: Canonical value is rendered as expected.
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
        """
        Assert that an http: Canonical value is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_CANONICAL": "http://spam.eggs/bacon"
            }
        )

    def test_config_canonical_scheme_invalid(self):
        """
        Assert that a Canonical value with an unrecognized scheme is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_CANONICAL": "ham://spam.eggs/bacon"
            }
        )

    def test_config_canonical_scheme_absent(self):
        """
        Assert that a Canonical value without a scheme is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_CANONICAL": "spam"
            }
        )

    def test_config_policy_default(self):
        """
        Assert that no Policy line is rendered by default.
        """
        self.assertLineAbsent(line_prefix="Policy:")

    def test_config_policy_https(self):
        """
        Assert that an https: Policy value is rendered as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_POLICY": "https://spam.eggs/bacon"
            },
            lines=[
                "Policy: https://spam.eggs/bacon"
            ]
        )

    def test_config_policy_http_invalid(self):
        """
        Assert that an http: Policy value is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_POLICY": "http://spam.eggs/bacon"
            }
        )

    def test_config_policy_scheme_invalid(self):
        """
        Assert that a Policy value with an unrecognized scheme is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_POLICY": "ham://spam.eggs/bacon"
            }
        )

    def test_config_policy_scheme_absent(self):
        """
        Assert that a Policy value without a scheme is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_POLICY": "spam"
            }
        )

    def test_config_hiring_default(self):
        """
        Assert that no Hiring: line is rendered by default.
        """
        self.assertLineAbsent(line_prefix="Hiring:")

    def test_config_hiring_https(self):
        """
        Assert that an https: Hiring value is rendered as expected.
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
        Assert that an http: Hiring value is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_HIRING": "http://spam.eggs/bacon"
            }
        )

    def test_config_hiring_scheme_invalid(self):
        """
        Assert that a Hiring value with an unrecognized scheme is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_HIRING": "ham://spam.eggs/bacon"
            }
        )

    def test_config_hiring_scheme_absent(self):
        """
        Assert that a Hiring value without a scheme is invalid.
        """
        self.assertHTTPStatus(
            expected_status_code=500,
            app_config={
                "SECURITY_TXT_HIRING": "spam"
            }
        )

    def test_config_field_case_default(self):
        """
        Assert that fields use standard case by default.
        """
        self.assertLinesMatch(lines=["Contact: mailto:security@localhost"])

    def test_config_field_case_standard(self):
        """
        Assert that SECURITY_TXT_FIELD_CASE "standard" renders fields as expected.
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
        Assert that SECURITY_TXT_FIELD_CASE "lower" renders fields as expected.
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
        Assert that SECURITY_TXT_FIELD_CASE "upper" renders fields as expected.
        """
        self.assertLinesMatch(
            app_config={
                "SECURITY_TXT_FIELD_CASE": "upper"
            },
            lines=[
                "CONTACT: mailto:security@localhost"
            ]
        )
