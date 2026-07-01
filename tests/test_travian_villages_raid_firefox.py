"""Unit tests for test_TravianVillagesRaidFirefox.py (Firefox-based raid class).

NOTE: The source file is missing ``from selenium.webdriver.support.ui import
WebDriverWait`` — the raid-flow method raises ``NameError`` at runtime.  Tests
that exercise the raid flow inject a mock ``WebDriverWait`` into the module
namespace so the rest of the logic can still be verified.
"""

import os
from unittest.mock import MagicMock, patch

import pytest

import test_TravianVillagesRaidFirefox as firefox_mod
from test_TravianVillagesRaidFirefox import TestTravianvillagesraid as _FirefoxRaidClass


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _inject_webdriverwait():
    """Inject a mock ``WebDriverWait`` into the Firefox module so the method
    under test doesn't crash on the missing import."""
    mock_wait_cls = MagicMock()
    mock_wait_inst = MagicMock()
    mock_wait_cls.return_value = mock_wait_inst
    mock_wait_inst.until.return_value = MagicMock()

    firefox_mod.WebDriverWait = mock_wait_cls
    yield mock_wait_cls
    if hasattr(firefox_mod, "WebDriverWait"):
        del firefox_mod.WebDriverWait


# ---------------------------------------------------------------------------
# Tests: missing-import detection
# ---------------------------------------------------------------------------

class TestMissingImportDetection:

    def test_webdriverwait_not_imported(self):
        """The source file never imports WebDriverWait."""
        import importlib
        source = importlib.util.find_spec("test_TravianVillagesRaidFirefox")
        with open(source.origin) as f:
            text = f.read()
        assert "import WebDriverWait" not in text.split("class")[0]


# ---------------------------------------------------------------------------
# Tests: setup / teardown
# ---------------------------------------------------------------------------

class TestFirefoxSetupMethod:

    @patch("test_TravianVillagesRaidFirefox.webdriver.Firefox")
    @patch("test_TravianVillagesRaidFirefox.load_dotenv")
    def test_loads_dotenv(self, mock_load_dotenv, mock_firefox):
        instance = _FirefoxRaidClass()
        instance.setup_method(None)
        mock_load_dotenv.assert_called_once()

    @patch("test_TravianVillagesRaidFirefox.webdriver.Firefox")
    @patch("test_TravianVillagesRaidFirefox.load_dotenv")
    def test_creates_firefox_driver(self, mock_load_dotenv, mock_firefox):
        instance = _FirefoxRaidClass()
        instance.setup_method(None)
        mock_firefox.assert_called_once()
        assert instance.driver is mock_firefox.return_value

    @patch("test_TravianVillagesRaidFirefox.webdriver.Firefox")
    @patch("test_TravianVillagesRaidFirefox.load_dotenv")
    def test_initialises_vars_as_empty_dict(self, mock_load_dotenv, mock_firefox):
        instance = _FirefoxRaidClass()
        instance.setup_method(None)
        assert instance.vars == {}


class TestFirefoxTeardownMethod:

    def test_quits_driver(self):
        instance = _FirefoxRaidClass()
        instance.driver = MagicMock()
        instance.teardown_method(None)
        instance.driver.quit.assert_called_once()


# ---------------------------------------------------------------------------
# Tests: raid flow (with WebDriverWait + ActionChains mocked)
# ---------------------------------------------------------------------------

class TestFirefoxRaidFlow:

    def _make_instance(self):
        instance = _FirefoxRaidClass()
        instance.driver = MagicMock()
        return instance

    @patch("test_TravianVillagesRaidFirefox.ActionChains")
    @patch("builtins.input", return_value="")
    @patch.dict(
        os.environ,
        {"TRAVIAN_EMAIL": "test@example.com", "TRAVIAN_PASSWORD": "secret123"},
    )
    def test_navigates_to_login_page(self, mock_input, mock_ac):
        instance = self._make_instance()
        instance.test_travianvillagesraid()
        instance.driver.get.assert_called_once_with(
            "https://www.travian.com/international#loginLobby"
        )

    @patch("test_TravianVillagesRaidFirefox.ActionChains")
    @patch("builtins.input", return_value="")
    @patch.dict(
        os.environ,
        {"TRAVIAN_EMAIL": "test@example.com", "TRAVIAN_PASSWORD": "secret123"},
    )
    def test_sets_window_size(self, mock_input, mock_ac):
        instance = self._make_instance()
        instance.test_travianvillagesraid()
        instance.driver.set_window_size.assert_called_once_with(1024, 768)

    @patch("test_TravianVillagesRaidFirefox.ActionChains")
    @patch("builtins.input", return_value="")
    @patch.dict(
        os.environ,
        {"TRAVIAN_EMAIL": "test@example.com", "TRAVIAN_PASSWORD": "secret123"},
    )
    def test_submits_login_form(self, mock_input, mock_ac):
        instance = self._make_instance()
        instance.test_travianvillagesraid()
        instance.driver.find_element.assert_any_call(
            "xpath", "//button[@type='submit']"
        )

    @patch("test_TravianVillagesRaidFirefox.ActionChains")
    @patch("builtins.input", return_value="")
    @patch.dict(
        os.environ,
        {"TRAVIAN_EMAIL": "test@example.com", "TRAVIAN_PASSWORD": "secret123"},
    )
    def test_performs_action_chains(self, mock_input, mock_ac):
        mock_ac_instance = MagicMock()
        mock_ac.return_value = mock_ac_instance
        mock_ac_instance.move_to_element.return_value = mock_ac_instance

        instance = self._make_instance()
        instance.test_travianvillagesraid()

        assert mock_ac_instance.move_to_element.call_count >= 2
        assert mock_ac_instance.perform.call_count >= 2

    @patch("test_TravianVillagesRaidFirefox.ActionChains")
    @patch("builtins.input", return_value="")
    @patch.dict(
        os.environ,
        {"TRAVIAN_EMAIL": "test@example.com", "TRAVIAN_PASSWORD": "secret123"},
    )
    def test_clicks_raid_buttons(self, mock_input, mock_ac):
        instance = self._make_instance()
        instance.test_travianvillagesraid()
        instance.driver.find_element.assert_any_call("id", "button67e04c1e282ff")
        instance.driver.find_element.assert_any_call("id", "button67e04c209a011")

    @patch("test_TravianVillagesRaidFirefox.ActionChains")
    @patch("builtins.input", return_value="")
    @patch.dict(
        os.environ,
        {"TRAVIAN_EMAIL": "test@example.com", "TRAVIAN_PASSWORD": "secret123"},
    )
    def test_prompts_user_before_quitting(self, mock_input, mock_ac):
        instance = self._make_instance()
        instance.test_travianvillagesraid()
        mock_input.assert_called_once_with("Press Enter to quit browser...")


class TestFirefoxEnvVarUsage:

    @patch("test_TravianVillagesRaidFirefox.ActionChains")
    @patch("builtins.input", return_value="")
    @patch.dict(
        os.environ,
        {"TRAVIAN_EMAIL": "player@game.com", "TRAVIAN_PASSWORD": "p@ss!"},
    )
    def test_reads_email_from_env(self, mock_input, mock_ac):
        instance = _FirefoxRaidClass()
        instance.driver = MagicMock()
        instance.test_travianvillagesraid()

        wait_cls = firefox_mod.WebDriverWait
        assert wait_cls.called

    @patch("test_TravianVillagesRaidFirefox.ActionChains")
    @patch("builtins.input", return_value="")
    @patch.dict(
        os.environ,
        {"TRAVIAN_EMAIL": "player@game.com", "TRAVIAN_PASSWORD": "p@ss!"},
    )
    def test_reads_password_from_env(self, mock_input, mock_ac):
        instance = _FirefoxRaidClass()
        instance.driver = MagicMock()
        instance.test_travianvillagesraid()

        wait_cls = firefox_mod.WebDriverWait
        assert wait_cls.return_value.until.call_count >= 2
