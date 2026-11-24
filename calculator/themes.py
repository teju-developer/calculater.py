"""
Themes module for Scientific Calculator.
Provides Midnight Purple, Ocean Blue, and Light Minimal visual themes
with persistent configuration saving.
"""

import json
import os
from typing import Callable, Dict, List


THEMES: Dict[str, Dict[str, str]] = {
    "midnight_purple": {
        "name": "Midnight Purple",
        "icon": "🔮",
        # Window & Canvas
        "bg_app": "#0c0a14",
        "bg_surface": "#141122",
        "bg_display": "#100d1e",
        "border_color": "#261f42",
        "fg_text": "#f8fafc",
        "fg_muted": "#94a3b8",
        # Accents
        "accent_primary": "#8b5cf6",
        "accent_secondary": "#a855f7",
        "accent_highlight": "#06b6d4",
        "accent_glow": "#3b1d6e",
        # Numbers
        "btn_num_bg": "#1c1830",
        "btn_num_fg": "#f1f5f9",
        "btn_num_hover": "#292347",
        # Basic Operators
        "btn_op_bg": "#251d3d",
        "btn_op_fg": "#c084fc",
        "btn_op_hover": "#362a57",
        # Scientific Operators
        "btn_sci_bg": "#161329",
        "btn_sci_fg": "#38bdf8",
        "btn_sci_hover": "#221c3d",
        # Action (AC, DEL)
        "btn_action_bg": "#311822",
        "btn_action_fg": "#f87171",
        "btn_action_hover": "#46202f",
        # Equal
        "btn_equal_bg": "#7c3aed",
        "btn_equal_fg": "#ffffff",
        "btn_equal_hover": "#6d28d9",
        # Memory
        "btn_mem_bg": "#18142b",
        "btn_mem_fg": "#cbd5e1",
        "btn_mem_hover": "#241e3d",
        # History panel
        "history_bg": "#100d1c",
        "history_card_bg": "#18142a",
        "history_card_hover": "#231d3d",
    },
    "ocean_blue": {
        "name": "Ocean Blue",
        "icon": "🌊",
        # Window & Canvas
        "bg_app": "#070d19",
        "bg_surface": "#0d1829",
        "bg_display": "#091220",
        "border_color": "#172a45",
        "fg_text": "#f0f9ff",
        "fg_muted": "#7dd3fc",
        # Accents
        "accent_primary": "#0284c7",
        "accent_secondary": "#00f2fe",
        "accent_highlight": "#38bdf8",
        "accent_glow": "#0c3b63",
        # Numbers
        "btn_num_bg": "#112239",
        "btn_num_fg": "#f8fafc",
        "btn_num_hover": "#193152",
        # Basic Operators
        "btn_op_bg": "#152c4a",
        "btn_op_fg": "#38bdf8",
        "btn_op_hover": "#1d3d66",
        # Scientific Operators
        "btn_sci_bg": "#0e1d32",
        "btn_sci_fg": "#22d3ee",
        "btn_sci_hover": "#172d4c",
        # Action (AC, DEL)
        "btn_action_bg": "#2c1722",
        "btn_action_fg": "#fb7185",
        "btn_action_hover": "#422030",
        # Equal
        "btn_equal_bg": "#0284c7",
        "btn_equal_fg": "#ffffff",
        "btn_equal_hover": "#0369a1",
        # Memory
        "btn_mem_bg": "#0f2036",
        "btn_mem_fg": "#bae6fd",
        "btn_mem_hover": "#172f4e",
        # History panel
        "history_bg": "#08101e",
        "history_card_bg": "#0f2038",
        "history_card_hover": "#172f4f",
    },
    "light_minimal": {
        "name": "Light Minimal",
        "icon": "☀️",
        # Window & Canvas
        "bg_app": "#f1f5f9",
        "bg_surface": "#ffffff",
        "bg_display": "#f8fafc",
        "border_color": "#cbd5e1",
        "fg_text": "#0f172a",
        "fg_muted": "#64748b",
        # Accents
        "accent_primary": "#4f46e5",
        "accent_secondary": "#6366f1",
        "accent_highlight": "#0ea5e9",
        "accent_glow": "#e0e7ff",
        # Numbers
        "btn_num_bg": "#ffffff",
        "btn_num_fg": "#0f172a",
        "btn_num_hover": "#f1f5f9",
        # Basic Operators
        "btn_op_bg": "#ede9fe",
        "btn_op_fg": "#6d28d9",
        "btn_op_hover": "#ddd6fe",
        # Scientific Operators
        "btn_sci_bg": "#f8fafc",
        "btn_sci_fg": "#0284c7",
        "btn_sci_hover": "#e2e8f0",
        # Action (AC, DEL)
        "btn_action_bg": "#fee2e2",
        "btn_action_fg": "#dc2626",
        "btn_action_hover": "#fecaca",
        # Equal
        "btn_equal_bg": "#4f46e5",
        "btn_equal_fg": "#ffffff",
        "btn_equal_hover": "#4338ca",
        # Memory
        "btn_mem_bg": "#f1f5f9",
        "btn_mem_fg": "#475569",
        "btn_mem_hover": "#e2e8f0",
        # History panel
        "history_bg": "#f8fafc",
        "history_card_bg": "#ffffff",
        "history_card_hover": "#f1f5f9",
    },
}


class ThemeManager:
    """Manages application theming and state persistence."""

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(config_dir, "theme_config.json")
        self.config_path = config_path
        self._theme_keys = list(THEMES.keys())
        self.current_theme_key = self._load_saved_theme()
        self._listeners: List[Callable[[Dict[str, str]], None]] = []

    def _load_saved_theme(self) -> str:
        """Load saved theme key from JSON config file if present."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    theme = data.get("theme")
                    if theme in THEMES:
                        return theme
        except Exception:
            pass
        return "midnight_purple"

    def _save_current_theme(self) -> None:
        """Persist current theme key to disk."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump({"theme": self.current_theme_key}, f, indent=2)
        except Exception:
            pass

    @property
    def current(self) -> Dict[str, str]:
        """Return the current theme color palette dictionary."""
        return THEMES[self.current_theme_key]

    @property
    def current_name(self) -> str:
        return THEMES[self.current_theme_key]["name"]

    @property
    def current_icon(self) -> str:
        return THEMES[self.current_theme_key]["icon"]

    def set_theme(self, theme_key: str) -> bool:
        """Set active theme by key."""
        if theme_key in THEMES:
            self.current_theme_key = theme_key
            self._save_current_theme()
            self._notify_listeners()
            return True
        return False

    def cycle_theme(self) -> str:
        """Cycle to the next theme in the list."""
        curr_idx = self._theme_keys.index(self.current_theme_key)
        next_idx = (curr_idx + 1) % len(self._theme_keys)
        self.set_theme(self._theme_keys[next_idx])
        return self.current_theme_key

    def add_listener(self, callback: Callable[[Dict[str, str]], None]) -> None:
        """Register a callback for theme change events."""
        if callback not in self._listeners:
            self._listeners.append(callback)

    def _notify_listeners(self) -> None:
        """Notify all registered listeners with the updated theme dictionary."""
        theme_data = self.current
        for listener in self._listeners:
            try:
                listener(theme_data)
            except Exception:
                pass
