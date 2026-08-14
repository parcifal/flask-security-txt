"""
Test the Flask-SecurityTxt configuration for the Acknowledgements field.
"""
from test import FlaskSecurityTxtTestCase


class TestConfigAcknowledgements(FlaskSecurityTxtTestCase):
    """
    A test class for validating the acknowledgement-related configuration in
    Flask-SecurityTxt.
    """

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
