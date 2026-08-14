"""
Test the Flask-SecurityTxt configuration for the field case setting.
"""
from test import FlaskSecurityTxtTestCase


class TestConfigFieldCase(FlaskSecurityTxtTestCase):
    """
    A test class for validating the field case-related configuration in
    Flask-SecurityTxt.
    """

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
