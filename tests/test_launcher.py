"""Unit tests for launcher.py.

launcher.py is a stub that checks ``option == 12`` and calls
``manual_coordinate_raider()``. We test the conditional logic and the
function call.
"""

from unittest.mock import MagicMock, patch

import pytest


class TestLauncherOption12:
    """Verify the option-12 branch in launcher.py."""

    def test_calls_manual_coordinate_raider_when_option_is_12(self):
        mock_raider = MagicMock()

        # The script references bare names ``option`` and
        # ``manual_coordinate_raider``; inject them via builtins so the
        # module-level code can resolve them.
        import builtins

        builtins.option = 12
        builtins.manual_coordinate_raider = mock_raider

        import importlib
        import sys

        sys.modules.pop("launcher", None)

        try:
            import launcher  # noqa: F401
        finally:
            del builtins.option
            del builtins.manual_coordinate_raider
            sys.modules.pop("launcher", None)

        mock_raider.assert_called_once()

    def test_does_not_call_raider_when_option_is_not_12(self):
        mock_raider = MagicMock()

        import builtins

        builtins.option = 5
        builtins.manual_coordinate_raider = mock_raider

        import sys

        sys.modules.pop("launcher", None)

        try:
            import launcher  # noqa: F401
        finally:
            del builtins.option
            del builtins.manual_coordinate_raider
            sys.modules.pop("launcher", None)

        mock_raider.assert_not_called()
