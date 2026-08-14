"""
A test case for the Flask-SecurityTxt extension.
"""
from .flask_security_txt_test_case import FlaskSecurityTxtTestCase


class TestFlaskSecurityTxt(FlaskSecurityTxtTestCase):
    """
    Test case for the Flask-SecurityTxt extension, excluding test_config-related
    tests.
    """

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
