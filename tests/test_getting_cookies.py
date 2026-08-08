"""Unit tests for gettingCookies.py (cookie saving script).

gettingCookies.py is a top-level script (no functions/classes), so we test it
by executing it as a module with the relevant side-effects mocked out.
"""

import importlib
import json
import sys
from io import StringIO
from unittest.mock import MagicMock, mock_open, patch

import pytest


@pytest.fixture(autouse=True)
def _clean_module_cache():
    """Remove the module from sys.modules before each test so it re-executes."""
    sys.modules.pop("gettingCookies", None)
    yield
    sys.modules.pop("gettingCookies", None)


class TestCookieScript:
    """Tests for the gettingCookies script behaviour."""

    @patch("time.sleep")
    @patch("builtins.open", new_callable=mock_open)
    def test_navigates_to_travian_login(self, mocked_file, mock_sleep):
        mock_driver = MagicMock()
        mock_driver.get_cookies.return_value = []

        with patch("selenium.webdriver.Chrome", return_value=mock_driver), \
             patch("selenium.webdriver.chrome.service.Service"):
            import gettingCookies  # noqa: F401

        mock_driver.get.assert_called_once_with(
            "https://www.travian.com/international#loginLobby"
        )

    @patch("time.sleep")
    @patch("builtins.open", new_callable=mock_open)
    def test_waits_for_manual_login(self, mocked_file, mock_sleep):
        mock_driver = MagicMock()
        mock_driver.get_cookies.return_value = []

        with patch("selenium.webdriver.Chrome", return_value=mock_driver), \
             patch("selenium.webdriver.chrome.service.Service"):
            import gettingCookies  # noqa: F401

        mock_sleep.assert_called_once_with(30)

    @patch("time.sleep")
    @patch("builtins.open", new_callable=mock_open)
    def test_saves_cookies_to_json_file(self, mocked_file, mock_sleep):
        fake_cookies = [
            {"name": "session_id", "value": "abc123"},
            {"name": "lang", "value": "en"},
        ]
        mock_driver = MagicMock()
        mock_driver.get_cookies.return_value = fake_cookies

        with patch("selenium.webdriver.Chrome", return_value=mock_driver), \
             patch("selenium.webdriver.chrome.service.Service"):
            import gettingCookies  # noqa: F401

        mocked_file.assert_called_once_with("travian_cookies.json", "w")

        written_data = "".join(
            c.args[0] for c in mocked_file().write.call_args_list
        )
        assert json.loads(written_data) == fake_cookies

    @patch("time.sleep")
    @patch("builtins.open", new_callable=mock_open)
    def test_quits_driver_after_saving(self, mocked_file, mock_sleep):
        mock_driver = MagicMock()
        mock_driver.get_cookies.return_value = []

        with patch("selenium.webdriver.Chrome", return_value=mock_driver), \
             patch("selenium.webdriver.chrome.service.Service"):
            import gettingCookies  # noqa: F401

        mock_driver.quit.assert_called_once()

    @patch("time.sleep")
    @patch("builtins.open", new_callable=mock_open)
    def test_cookies_file_uses_indent_2(self, mocked_file, mock_sleep):
        mock_driver = MagicMock()
        mock_driver.get_cookies.return_value = [{"name": "x", "value": "1"}]

        with patch("selenium.webdriver.Chrome", return_value=mock_driver), \
             patch("selenium.webdriver.chrome.service.Service"):
            import gettingCookies  # noqa: F401

        written = "".join(
            c.args[0] for c in mocked_file().write.call_args_list
        )
        # indent=2 produces multi-line output with two-space indentation
        assert "\n  " in written
