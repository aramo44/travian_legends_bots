"""Unit tests for VillageOasisRaidRecording.py (Chrome-based raid class)."""

import os
from unittest.mock import MagicMock, patch, call

import pytest

from VillageOasisRaidRecording import TestTravianvillagesraid as _ChromeRaidClass


class TestSetupMethod:
    """Tests for TestTravianvillagesraid.setup_method."""

    @patch("VillageOasisRaidRecording.webdriver.Chrome")
    @patch("VillageOasisRaidRecording.load_dotenv")
    def test_loads_dotenv(self, mock_load_dotenv, mock_chrome):
        instance = _ChromeRaidClass()
        instance.setup_method(None)

        mock_load_dotenv.assert_called_once()

    @patch("VillageOasisRaidRecording.webdriver.Chrome")
    @patch("VillageOasisRaidRecording.load_dotenv")
    def test_creates_chrome_driver_with_options(self, mock_load_dotenv, mock_chrome):
        instance = _ChromeRaidClass()
        instance.setup_method(None)

        mock_chrome.assert_called_once()
        _, kwargs = mock_chrome.call_args
        assert "service" in kwargs
        assert "options" in kwargs

    @patch("VillageOasisRaidRecording.webdriver.Chrome")
    @patch("VillageOasisRaidRecording.load_dotenv")
    def test_chrome_options_include_start_maximized(
        self, mock_load_dotenv, mock_chrome
    ):
        instance = _ChromeRaidClass()

        with patch("VillageOasisRaidRecording.Options") as mock_options_cls:
            mock_opts = MagicMock()
            mock_options_cls.return_value = mock_opts
            instance.setup_method(None)

            mock_opts.add_argument.assert_any_call("start-maximized")

    @patch("VillageOasisRaidRecording.webdriver.Chrome")
    @patch("VillageOasisRaidRecording.load_dotenv")
    def test_initialises_vars_as_empty_dict(self, mock_load_dotenv, mock_chrome):
        instance = _ChromeRaidClass()
        instance.setup_method(None)

        assert instance.vars == {}


class TestTeardownMethod:
    """Tests for TestTravianvillagesraid.teardown_method."""

    def test_quits_driver(self):
        instance = _ChromeRaidClass()
        instance.driver = MagicMock()

        instance.teardown_method(None)

        instance.driver.quit.assert_called_once()


class TestRaidFlow:
    """Tests for TestTravianvillagesraid.test_travianvillagesraid."""

    @patch("VillageOasisRaidRecording.WebDriverWait")
    @patch("VillageOasisRaidRecording.ActionChains")
    @patch("builtins.input", return_value="")
    @patch.dict(
        os.environ,
        {"TRAVIAN_EMAIL": "test@example.com", "TRAVIAN_PASSWORD": "secret123"},
    )
    def test_navigates_to_login_page(self, mock_input, mock_actions, mock_wait):
        instance = _ChromeRaidClass()
        instance.driver = MagicMock()

        # Make WebDriverWait.until return a mock element
        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        mock_wait_instance.until.return_value = MagicMock()

        instance.test_travianvillagesraid()

        instance.driver.get.assert_called_once_with(
            "https://www.travian.com/international#loginLobby"
        )

    @patch("VillageOasisRaidRecording.WebDriverWait")
    @patch("VillageOasisRaidRecording.ActionChains")
    @patch("builtins.input", return_value="")
    @patch.dict(
        os.environ,
        {"TRAVIAN_EMAIL": "test@example.com", "TRAVIAN_PASSWORD": "secret123"},
    )
    def test_sends_email_credentials(self, mock_input, mock_actions, mock_wait):
        instance = _ChromeRaidClass()
        instance.driver = MagicMock()

        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        mock_element = MagicMock()
        mock_wait_instance.until.return_value = mock_element

        instance.test_travianvillagesraid()

        mock_element.send_keys.assert_any_call("test@example.com")

    @patch("VillageOasisRaidRecording.WebDriverWait")
    @patch("VillageOasisRaidRecording.ActionChains")
    @patch("builtins.input", return_value="")
    @patch.dict(
        os.environ,
        {"TRAVIAN_EMAIL": "test@example.com", "TRAVIAN_PASSWORD": "secret123"},
    )
    def test_sends_password_credentials(self, mock_input, mock_actions, mock_wait):
        instance = _ChromeRaidClass()
        instance.driver = MagicMock()

        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        mock_element = MagicMock()
        mock_wait_instance.until.return_value = mock_element

        instance.test_travianvillagesraid()

        mock_element.send_keys.assert_any_call("secret123")

    @patch("VillageOasisRaidRecording.WebDriverWait")
    @patch("VillageOasisRaidRecording.ActionChains")
    @patch("builtins.input", return_value="")
    @patch.dict(
        os.environ,
        {"TRAVIAN_EMAIL": "test@example.com", "TRAVIAN_PASSWORD": "secret123"},
    )
    def test_clicks_submit_button(self, mock_input, mock_actions, mock_wait):
        instance = _ChromeRaidClass()
        instance.driver = MagicMock()

        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        mock_wait_instance.until.return_value = MagicMock()

        instance.test_travianvillagesraid()

        # Verify that find_element was called with the submit button XPATH
        instance.driver.find_element.assert_any_call(
            "xpath", "//button[@type='submit']"
        )

    @patch("VillageOasisRaidRecording.WebDriverWait")
    @patch("VillageOasisRaidRecording.ActionChains")
    @patch("builtins.input", return_value="")
    @patch.dict(
        os.environ,
        {"TRAVIAN_EMAIL": "test@example.com", "TRAVIAN_PASSWORD": "secret123"},
    )
    def test_performs_action_chains_for_navigation(
        self, mock_input, mock_actions, mock_wait
    ):
        instance = _ChromeRaidClass()
        instance.driver = MagicMock()

        mock_actions_instance = MagicMock()
        mock_actions.return_value = mock_actions_instance
        mock_actions_instance.move_to_element.return_value = mock_actions_instance

        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        mock_wait_instance.until.return_value = MagicMock()

        instance.test_travianvillagesraid()

        assert mock_actions_instance.move_to_element.call_count >= 2
        assert mock_actions_instance.perform.call_count >= 2

    @patch("VillageOasisRaidRecording.WebDriverWait")
    @patch("VillageOasisRaidRecording.ActionChains")
    @patch("builtins.input", return_value="")
    @patch.dict(
        os.environ,
        {"TRAVIAN_EMAIL": "test@example.com", "TRAVIAN_PASSWORD": "secret123"},
    )
    def test_prompts_user_before_quitting(self, mock_input, mock_actions, mock_wait):
        instance = _ChromeRaidClass()
        instance.driver = MagicMock()

        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        mock_wait_instance.until.return_value = MagicMock()

        instance.test_travianvillagesraid()

        mock_input.assert_called_once_with("Press Enter to quit browser...")


class TestMainBlock:
    """Tests for the __main__ execution block."""

    @patch("VillageOasisRaidRecording.WebDriverWait")
    @patch("VillageOasisRaidRecording.ActionChains")
    @patch("VillageOasisRaidRecording.webdriver.Chrome")
    @patch("VillageOasisRaidRecording.load_dotenv")
    @patch("builtins.input", return_value="")
    @patch.dict(
        os.environ,
        {"TRAVIAN_EMAIL": "test@example.com", "TRAVIAN_PASSWORD": "secret123"},
    )
    def test_teardown_called_even_on_error(
        self, mock_input, mock_load_dotenv, mock_chrome, mock_actions, mock_wait
    ):
        """Verify teardown_method is called even if test_travianvillagesraid raises."""
        instance = _ChromeRaidClass()
        instance.setup_method(None)

        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        mock_wait_instance.until.side_effect = Exception("element not found")

        with pytest.raises(Exception, match="element not found"):
            try:
                instance.test_travianvillagesraid()
            finally:
                instance.teardown_method(None)

        instance.driver.quit.assert_called_once()
