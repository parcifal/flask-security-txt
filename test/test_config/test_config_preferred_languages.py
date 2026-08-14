"""
Test the Flask-SecurityTxt configuration for the Preferred Languages field.
"""
from test import FlaskSecurityTxtTestCase


class TestConfigPreferredLanguages(FlaskSecurityTxtTestCase):
    """
    A test class for validating the preferred languages-related configuration
    in Flask-SecurityTxt.
    """

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
