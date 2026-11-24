"""
Unit Tests for Calculation History Manager.
"""

import os
import tempfile
import unittest

from calculator.history import HistoryManager


class TestHistoryManager(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        self.history = HistoryManager(storage_path=self.temp_file.name, max_entries=5)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            try:
                os.remove(self.temp_file.name)
            except Exception:
                pass

    def test_add_and_retrieve_entries(self):
        self.history.add_entry("2 + 2", "4")
        self.history.add_entry("sin(30)", "0.5")

        entries = self.history.get_entries()
        self.assertEqual(len(entries), 2)
        # Recent first
        self.assertEqual(entries[0]["expression"], "sin(30)")
        self.assertEqual(entries[0]["result"], "0.5")
        self.assertEqual(entries[1]["expression"], "2 + 2")
        self.assertEqual(entries[1]["result"], "4")

    def test_max_entries_truncation(self):
        for i in range(10):
            self.history.add_entry(f"expr_{i}", f"{i}")
        entries = self.history.get_entries()
        self.assertEqual(len(entries), 5)
        self.assertEqual(entries[0]["expression"], "expr_9")

    def test_clear_history(self):
        self.history.add_entry("10 * 10", "100")
        self.assertEqual(len(self.history.get_entries()), 1)
        self.history.clear()
        self.assertEqual(len(self.history.get_entries()), 0)

    def test_persistence(self):
        self.history.add_entry("sqrt(144)", "12")
        # Load in another instance from same path
        new_history = HistoryManager(storage_path=self.temp_file.name, max_entries=5)
        entries = new_history.get_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["result"], "12")


if __name__ == "__main__":
    unittest.main()
