"""
calculater.py - Upgraded Entry Point
Backward-compatible wrapper for QuantumCalc Advanced Scientific Calculator.
Upgraded from the original basic calculator to modern modular architecture.
"""

import sys
import os
import tkinter as tk

# Ensure current directory is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import enable_high_dpi_awareness
from calculator.ui import CalculatorUI


class Calculator(CalculatorUI):
    """
    Backward-compatible Calculator class extending the modernized CalculatorUI.
    Allows existing code referencing Calculator(root) to function seamlessly.
    """
    def __init__(self, master=None):
        if master is None:
            master = tk.Tk()
        super().__init__(master)


def main():
    enable_high_dpi_awareness()
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
