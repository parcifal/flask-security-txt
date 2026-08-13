"""
Test the Flask-SecurityTxt configuration for the Policy field.
"""
from test import FlaskSecurityTxtTestCase


class TestConfigPolicy(FlaskSecurityTxtTestCase):
    """
    A test class for validating the policy-related configuration in
    Flask-SecurityTxt.
    """

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
