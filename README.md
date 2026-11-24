# 🧮 QuantumCalc • Advanced Scientific Calculator

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![UI Framework](https://img.shields.io/badge/GUI-Tkinter%209.0-blueviolet.svg)](https://docs.python.org/3/library/tkinter.html)
[![Safety](https://img.shields.io/badge/Security-Safe%20AST%20Parser-emerald.svg)](https://docs.python.org/3/library/ast.html)
[![Tests](https://img.shields.io/badge/tests-22%20passed-success.svg)](./tests)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#)

> **QuantumCalc** is a professional desktop scientific calculator designed with modern UI/UX principles, an AST-based safe calculation engine, multi-theme support, persistent calculation history, and complete keyboard navigation.

---

## 🌟 Evolution & Background

This project began as a basic single-file Tkinter script (`calculater.py`) using fixed coordinates and Python's unrestricted `eval()`. 

Through this upgrade, it has been transformed into a desktop application featuring:
- **Modular Object-Oriented Architecture**: Clean separation between the calculation engine, UI components, theming engine, and state history.
- **Enterprise-Grade Expression Security**: Complete replacement of `eval()` with an **Abstract Syntax Tree (AST)** evaluator allowing only whitelisted mathematical operations.
- **Modern Futuristic Aesthetics**: Dark graphite & neon violet/cyan themes, custom canvas-rendered rounded buttons with smooth hover transitions, and responsive grid layouts.
- **High-DPI Display Optimization**: Crisp font rendering with Windows per-monitor DPI scaling.

---

## 📸 Screenshots & Themes

QuantumCalc includes three themes that can be switched on-the-fly without restarting:

| **Midnight Purple (Default)** | **Ocean Blue** | **Light Minimal** |
|:---:|:---:|:---:|
| ![Midnight Purple](assets/preview_midnight_purple.png) | ![Ocean Blue](assets/preview_ocean_blue.png) | ![Light Minimal](assets/preview_light_minimal.png) |
| *Deep obsidian graphite with electric violet & cyan accents* | *Abyssal navy blue with electric cyan highlights* | *Clean slate white with soft indigo & cobalt tones* |

---

## ✨ Features

### 1. 🛡️ Safe AST Calculation Engine
- **No Unsafe `eval()`**: Uses Python's `ast` module to construct an expression tree, recursively validating allowed operators, functions, and constants.
- **Malicious Code Rejection**: Arbitrary code execution, file operations, system calls, and attribute inspection (e.g. `__import__`, `open`, `globals`) are rejected.
- **Friendly Error Handling**: Gracefully handles `ZeroDivisionError`, `OverflowError`, `SyntaxError`, and domain errors (e.g., negative square roots, logarithms of non-positive numbers).
- **Smart Preprocessing**: Implicit multiplication (`2(3)` $\to$ `2*(3)`, `2pi` $\to$ `2*pi`), factorial notation (`5!` $\to$ `fact(5)`), and percentages (`50%` $\to$ `0.5`).

### 2. 🔬 Dual Calculator Modes (Standard & Scientific)
- **Standard Mode**: Streamlined layout for rapid everyday arithmetic ($+$, $-$, $\times$, $\div$, $\%$, parentheses, $\pm$).
- **Scientific Mode**: Expanded panel providing:
  - **Trigonometric**: $\sin$, $\cos$, $\tan$
  - **Inverse Trigonometric**: $\arcsin$, $\arccos$, $\arctan$
  - **Angle Units**: One-click **DEG** (Degrees) and **RAD** (Radians) switching with floating-point zero snapping for exact angles (e.g., $\cos(90^\circ) = 0$).
  - **Exponentials & Roots**: Square ($x^2$), Cube ($x^3$), Power ($x^y$), Square Root ($\sqrt{x}$), Cube Root ($\sqrt[3]{x}$).
  - **Logarithms**: Common logarithm ($\log_{10}$), Natural logarithm ($\ln$).
  - **Advanced Functions**: Factorial ($n!$), Absolute Value ($|x|$), Constants ($\pi$, $e$).

### 3. 🕒 Interactive Calculation History Drawer
- **Persistent Storage**: Previous calculations are saved to JSON disk storage and automatically restored across app sessions.
- **Reverse Chronological Order**: Most recent calculations appear first with timestamps.
- **Click-to-Reuse**: Click any history entry to immediately load its expression or result back into the active calculation.
- **History Management**: Clear all history with a single click.

### 4. 💾 Memory Functions
- **MC**: Memory Clear (Resets memory register to 0).
- **MR**: Memory Recall (Inserts stored memory value into current expression).
- **M+**: Memory Add (Adds current result to memory).
- **M-**: Memory Subtract (Subtracts current result from memory).
- **MS**: Memory Store (Stores current number in memory).
- **Live Memory Indicator**: Visible `[ M ]` badge lights up with active values when memory is stored.

### 5. ⌨️ Complete Keyboard Support
Operate the calculator using either mouse clicks or keyboard inputs:

| Key / Shortcut | Function | Key / Shortcut | Function |
|:---|:---|:---|:---|
| `0` – `9` | Number input | `Enter` or `=` | Calculate result |
| `+`, `-`, `*`, `/` | Arithmetic operators | `Backspace` | Delete last character |
| `(`, `)` | Parentheses | `Esc` or `Delete` | All Clear (AC) |
| `%` | Percentage / Modulo | `!` | Factorial |
| `^` | Power ($x^y$) | `.` | Decimal point |
| `Ctrl + S` | Toggle Scientific / Standard Mode | `Ctrl + H` | Toggle History Panel |
| `Ctrl + T` | Cycle Visual Theme | `Ctrl + R` | Toggle DEG / RAD Mode |

---

## 🏗️ Project Architecture

```
calculator-project/
│
├── main.py                     # Primary modern desktop application entry point
├── calculater.py               # Backward-compatible wrapper for original file
│
├── calculator/                 # Modular core package
│   ├── __init__.py             # Package descriptor & version metadata
│   ├── engine.py               # Safe AST mathematical parser & computation engine
│   ├── ui.py                   # Modern Tkinter UI, custom canvas buttons, tooltips
│   ├── themes.py               # 3 color palettes & theme persistence manager
│   └── history.py              # Calculation history persistence & event manager
│
├── assets/                     # Graphical assets & icons
│   ├── calculator_icon.ico     # Multi-resolution Windows app icon (256x256 to 16x16)
│   ├── calculator_icon.png     # High-res PNG logo
│   ├── preview_midnight_purple.png
│   ├── preview_ocean_blue.png
│   └── preview_light_minimal.png
│
├── tests/                      # Automated unit test suite
│   ├── test_engine.py          # 16 tests: arithmetic, scientific, AST security
│   ├── test_history.py         # 4 tests: persistence, ordering, truncation
│   └── test_themes.py          # 2 tests: palettes, cycling, theme config
│
├── requirements.txt            # Project dependencies (zero external dependencies required)
└── README.md                   # Complete documentation & engineering guide
```

---

## 🚀 Installation & Running

### Prerequisites
- Python **3.8+** (Python 3.10+ recommended)
- Standard library modules: `tkinter`, `ast`, `math`, `json`, `os`, `sys`, `ctypes` (all included with standard Python installations).

### 1. Clone or Open Project
```bash
git clone https://github.com/teju-developer/calculater.py.git
cd calculater.py
```

### 2. (Optional) Install Assets Tools
The calculator core uses only built-in standard libraries. To regenerate icons or capture screenshots:
```bash
pip install -r requirements.txt
```

### 3. Run the Calculator
You can launch the calculator using either entry point:

```bash
# Recommended modern entry point:
python main.py

# Or the original filename (fully preserved):
python calculater.py
```

---

## 🧪 Running Unit Tests

The test suite covers basic arithmetic, scientific formulas, trigonometric angle conversions, domain error handling, and code injection security attacks.

Run all tests via Python's built-in `unittest` runner:

```bash
python -m unittest discover tests
```

Sample output:
```text
......................
----------------------------------------------------------------------
Ran 22 tests in 0.036s

OK
```

---

## 🔒 Security Architecture: Safe AST vs `eval()`

| Feature | Legacy `eval()` | QuantumCalc AST Engine |
|:---|:---:|:---:|
| Arbitrary Code Execution | ❌ High Risk (`os.system`, `__import__`) | ✅ **Blocked** (Only Whitelisted Math Nodes) |
| Attribute / Class Traversal | ❌ Vulnerable (`.__class__.__bases__`) | ✅ **Rejected** at AST Node Inspection |
| File & Network Access | ❌ Unrestricted (`open()`, `socket`) | ✅ **Zero Access** |
| Infinite Loop / CPU Bomb | ❌ Can freeze host | ✅ **Protected** (Exponent & length limits) |
| Division / Modulo by Zero | ❌ Crashes application | ✅ **Friendly Error Message** |
| Trigonometric Domain Errors | ❌ Throws raw exception | ✅ **Clear Diagnostics** |

---

## 👤 Author & Portfolio
- **Developer**: Tejashwini ([teju-developer](https://github.com/teju-developer))
- **Project**: QuantumCalc Scientific Desktop Calculator
- **License**: MIT License
