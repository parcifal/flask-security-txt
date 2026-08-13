"""
Test the Flask-SecurityTxt configuration for the Expires field.
"""
from datetime import datetime as dt, timedelta as td, timezone as tz
from test import FlaskSecurityTxtTestCase


class TestConfigExpires(FlaskSecurityTxtTestCase):
    """
    A test class for validating the expires-related configuration in
    Flask-SecurityTxt.
    """

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
