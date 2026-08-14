"""
Test the Flask-SecurityTxt configuration for the Canonical field.
"""
from test import FlaskSecurityTxtTestCase


class TestConfigCanonical(FlaskSecurityTxtTestCase):
    """
    A test class for validating the canonical-related configuration in
    Flask-SecurityTxt.
    """

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
