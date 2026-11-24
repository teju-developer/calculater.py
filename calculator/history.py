"""
Calculation History Management Module.
Maintains history of mathematical evaluations with timestamps,
persistence, and listener callbacks for UI updates.
"""

from datetime import datetime
import json
import os
from typing import Any, Callable, Dict, List, Optional


class HistoryManager:
    """Manages calculator history storage, persistence, and change notifications."""

    def __init__(self, storage_path: Optional[str] = None, max_entries: int = 50):
        if storage_path is None:
            module_dir = os.path.dirname(os.path.abspath(__file__))
            storage_path = os.path.join(module_dir, "calculator_history.json")
        self.storage_path = storage_path
        self.max_entries = max_entries
        self._entries: List[Dict[str, Any]] = []
        self._listeners: List[Callable[[List[Dict[str, Any]]], None]] = []
        self.load_from_disk()

    def add_entry(self, expression: str, result: str) -> Dict[str, Any]:
        """
        Record a calculation. Recent calculations appear first.
        """
        entry = {
            "id": len(self._entries) + 1,
            "expression": expression.strip(),
            "result": str(result).strip(),
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%b %d"),
        }

        # Avoid immediate duplicate consecutive evaluations
        if self._entries and self._entries[0].get("expression") == entry["expression"] and self._entries[0].get("result") == entry["result"]:
            return self._entries[0]

        # Insert at beginning so most recent is first
        self._entries.insert(0, entry)

        # Truncate to maximum capacity
        if len(self._entries) > self.max_entries:
            self._entries = self._entries[: self.max_entries]

        self.save_to_disk()
        self._notify_listeners()
        return entry

    def get_entries(self) -> List[Dict[str, Any]]:
        """Return list of calculation records (recent first)."""
        return list(self._entries)

    def clear(self) -> None:
        """Clear all stored calculation history."""
        self._entries.clear()
        self.save_to_disk()
        self._notify_listeners()

    def add_listener(self, callback: Callable[[List[Dict[str, Any]]], None]) -> None:
        """Register a callback invoked when history changes."""
        if callback not in self._listeners:
            self._listeners.append(callback)

    def _notify_listeners(self) -> None:
        entries = self.get_entries()
        for listener in self._listeners:
            try:
                listener(entries)
            except Exception:
                pass

    def save_to_disk(self) -> None:
        """Save history to JSON file."""
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self._entries, f, indent=2)
        except Exception:
            pass

    def load_from_disk(self) -> None:
        """Load history from JSON file."""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self._entries = data[: self.max_entries]
        except Exception:
            self._entries = []
