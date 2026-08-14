"""
Test the Flask-SecurityTxt configuration for the Encryption field.
"""
from test import FlaskSecurityTxtTestCase


class TestConfigEncryption(FlaskSecurityTxtTestCase):
    """
    A test class for validating the encryption-related configuration in
    Flask-SecurityTxt.
    """

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
                "Encryption: openpgp4fpr:5F2DE5521600DEFA"
            ]
        )
