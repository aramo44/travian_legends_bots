"""Unit tests for seleniumTest.py (login script).

seleniumTest.py is a top-level script, so we import it under heavy mocking
to verify the browser automation steps it performs.
"""

import sys
from unittest.mock import MagicMock, patch, call

import pytest


@pytest.fixture(autouse=True)
def _clean_module_cache():
    """Remove the module from sys.modules before each test so it re-executes."""
    sys.modules.pop("seleniumTest", None)
    yield
    sys.modules.pop("seleniumTest", None)


def _import_with_mocks(mock_driver):
    """Import seleniumTest with a fully mocked Chrome driver."""
    mock_email = MagicMock()
    mock_password = MagicMock()
    mock_login_btn = MagicMock()

    def find_element_side_effect(by, value):
        if value == "password":
            return mock_password
        if value == "//button[@type='submit']":
            return mock_login_btn
        return MagicMock()

    mock_driver.find_element.side_effect = find_element_side_effect
    mock_driver.find_elements.return_value = []  # no iframes

    # WebDriverWait(...).until(...) returns the email field
    with patch("selenium.webdriver.Chrome", return_value=mock_driver), \
         patch("selenium.webdriver.chrome.service.Service"), \
         patch(
             "selenium.webdriver.support.ui.WebDriverWait"
         ) as mock_wait_cls, \
         patch("builtins.input", return_value=""):
        mock_wait_inst = MagicMock()
        mock_wait_cls.return_value = mock_wait_inst
        mock_wait_inst.until.return_value = mock_email

        import seleniumTest  # noqa: F401

    return mock_email, mock_password, mock_login_btn


class TestSeleniumLoginScript:
    """Tests for the seleniumTest.py script."""

    def test_navigates_to_travian_login(self):
        mock_driver = MagicMock()

        _import_with_mocks(mock_driver)

        mock_driver.get.assert_called_once_with(
            "https://www.travian.com/international#loginLobby"
        )

    def test_fills_in_email_field(self):
        mock_driver = MagicMock()
        mock_email, _, _ = _import_with_mocks(mock_driver)

        mock_email.send_keys.assert_called_once_with("your_email@example.com")

    def test_fills_in_password_field(self):
        mock_driver = MagicMock()
        _, mock_password, _ = _import_with_mocks(mock_driver)

        mock_password.send_keys.assert_called_once_with("your_password")

    def test_clicks_login_button(self):
        mock_driver = MagicMock()
        _, _, mock_login_btn = _import_with_mocks(mock_driver)

        mock_login_btn.click.assert_called_once()

    def test_lists_iframes(self):
        mock_driver = MagicMock()
        mock_iframe = MagicMock()
        mock_iframe.get_attribute.return_value = "test-frame"
        mock_driver.find_elements.return_value = [mock_iframe]

        _import_with_mocks(mock_driver)

        mock_driver.find_elements.assert_called_once_with("tag name", "iframe")

    def test_quits_driver_at_end(self):
        mock_driver = MagicMock()

        _import_with_mocks(mock_driver)

        mock_driver.quit.assert_called_once()

    def test_waits_for_user_input_before_quitting(self):
        mock_driver = MagicMock()

        with patch("selenium.webdriver.Chrome", return_value=mock_driver), \
             patch("selenium.webdriver.chrome.service.Service"), \
             patch("selenium.webdriver.support.ui.WebDriverWait") as mock_wc, \
             patch("builtins.input", return_value="") as mock_input:
            mock_wc.return_value.until.return_value = MagicMock()
            mock_driver.find_elements.return_value = []
            sys.modules.pop("seleniumTest", None)

            import seleniumTest  # noqa: F401

            mock_input.assert_called_once_with("Press Enter to quit...")
