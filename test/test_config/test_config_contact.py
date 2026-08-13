"""
Test the Flask-SecurityTxt configuration for the Contact field.
"""
from test import FlaskSecurityTxtTestCase


class TestConfigContact(FlaskSecurityTxtTestCase):
    """
    A test class for validating the contact-related configuration in
    Flask-SecurityTxt.
    """

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
