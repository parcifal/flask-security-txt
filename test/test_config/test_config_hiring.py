"""
Test the Flask-SecurityTxt configuration for the Hiring field.
"""
from test import FlaskSecurityTxtTestCase


class TestConfigHiring(FlaskSecurityTxtTestCase):
    """
    A test class for validating the hiring-related configuration in
    Flask-SecurityTxt.
    """

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
