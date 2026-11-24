"""
Unit Tests for Theme Manager.
"""

import os
import tempfile
import unittest

from calculator.themes import THEMES, ThemeManager


class TestThemeManager(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        self.manager = ThemeManager(config_path=self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            try:
                os.remove(self.temp_file.name)
            except Exception:
                pass

    def test_theme_keys_and_palettes(self):
        self.assertIn("midnight_purple", THEMES)
        self.assertIn("ocean_blue", THEMES)
        self.assertIn("light_minimal", THEMES)

        required_keys = [
            "name", "bg_app", "bg_surface", "bg_display", "fg_text",
            "accent_primary", "btn_num_bg", "btn_op_bg", "btn_sci_bg", "btn_equal_bg"
        ]
        for key, palette in THEMES.items():
            for req in required_keys:
                self.assertIn(req, palette, f"Theme '{key}' is missing required key '{req}'")

    def test_cycle_and_set_theme(self):
        self.manager.set_theme("midnight_purple")
        self.assertEqual(self.manager.current_theme_key, "midnight_purple")

        next_theme = self.manager.cycle_theme()
        self.assertNotEqual(next_theme, "midnight_purple")

        # Persistence test
        new_mgr = ThemeManager(config_path=self.temp_file.name)
        self.assertEqual(new_mgr.current_theme_key, next_theme)


if __name__ == "__main__":
    unittest.main()
