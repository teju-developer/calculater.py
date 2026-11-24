"""
calculater.py - Upgraded Entry Point
Backward-compatible wrapper for QuantumCalc Advanced Scientific Calculator.
Upgraded from the original basic calculator to modern modular architecture.
"""

import os
import sys

# Ensure current directory is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app, application, enable_high_dpi_awareness, handler


class Calculator:
    """
    Backward-compatible Calculator class extending the modernized CalculatorUI.
    Allows existing code referencing Calculator(root) to function seamlessly.
    """

    def __init__(self, master=None):
        import tkinter as tk
        from calculator.ui import CalculatorUI

        if master is None:
            master = tk.Tk()
        self.ui = CalculatorUI(master)


def main():
    enable_high_dpi_awareness()
    import tkinter as tk
    from calculator.ui import CalculatorUI

    root = tk.Tk()
    app_ui = CalculatorUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
