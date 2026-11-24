"""
QuantumCalc • Advanced Scientific Calculator
Main Application Entry Point.
"""

import ctypes
import os
import sys
import tkinter as tk

# Ensure calculator module is discoverable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculator.ui import CalculatorUI


def enable_high_dpi_awareness():
    """Enable high-DPI awareness on Windows for crystal-clear font rendering."""
    if sys.platform == "win32":
        try:
            # Per-monitor DPI aware (Windows 8.1+)
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            try:
                # System DPI aware (Windows Vista+)
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass


def main():
    """Initialize and run the QuantumCalc desktop application."""
    enable_high_dpi_awareness()
    root = tk.Tk()
    app = CalculatorUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
