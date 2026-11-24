"""
Modern Scientific Calculator UI module built with Tkinter.
Features:
- Futuristic dark graphite & neon aesthetic with 3 switchable themes
- Canvas-based custom rounded buttons with smooth hover & click animations
- Interactive tooltips for scientific functions
- Standard & Scientific modes with DEG/RAD switching
- Real-time memory indicators (MC, MR, M+, M-, MS)
- Collapsible interactive calculation history side drawer
- Comprehensive keyboard shortcuts & event bindings
"""

import math
import os
import sys
import tkinter as tk
from tkinter import font as tkfont
from typing import Any, Callable, Dict, List, Optional

from calculator.engine import CalculatorEngine
from calculator.history import HistoryManager
from calculator.themes import THEMES, ThemeManager


# Helper to draw smooth antialiased-looking rounded rectangles on Canvas
def draw_rounded_rectangle(canvas: tk.Canvas, x1: float, y1: float, x2: float, y2: float,
                           radius: float = 14, **kwargs) -> int:
    """Draw a smooth rounded rectangle on a Tkinter canvas."""
    # Ensure coordinates and radius are valid
    w = max(1, x2 - x1)
    h = max(1, y2 - y1)
    r = min(radius, w / 2, h / 2)
    if r < 1:
        return canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

    points = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


class Tooltip:
    """Lightweight modern tooltip for displaying scientific function hints."""

    def __init__(self, widget: tk.Widget, text: str, delay: int = 400):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip_window: Optional[tk.Toplevel] = None
        self._after_id: Optional[str] = None
        self.bg_color = "#1e1b2e"
        self.fg_color = "#e2e8f0"
        self.border_color = "#4c3d75"

        self.widget.bind("<Enter>", self._on_enter, add="+")
        self.widget.bind("<Leave>", self._on_leave, add="+")
        self.widget.bind("<ButtonPress>", self._on_leave, add="+")

    def set_colors(self, bg: str, fg: str, border: str) -> None:
        self.bg_color = bg
        self.fg_color = fg
        self.border_color = border

    def _on_enter(self, event=None) -> None:
        self._schedule()

    def _on_leave(self, event=None) -> None:
        self._cancel()
        self._hide()

    def _schedule(self) -> None:
        self._cancel()
        self._after_id = self.widget.after(self.delay, self._show)

    def _cancel(self) -> None:
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None

    def _show(self) -> None:
        if not self.text or self.tip_window:
            return

        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() - 32

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.attributes("-topmost", True)

        frame = tk.Frame(tw, bg=self.border_color, padx=1, pady=1)
        frame.pack()
        inner = tk.Frame(frame, bg=self.bg_color, padx=8, pady=4)
        inner.pack()

        label = tk.Label(
            inner,
            text=self.text,
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg=self.fg_color,
            justify=tk.LEFT
        )
        label.pack()

    def _hide(self) -> None:
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


class ModernButton(tk.Canvas):
    """
    Sleek, rounded custom button with smooth hover highlights,
    tactile click feedback, and vector graphics.
    """

    def __init__(
        self,
        master: tk.Widget,
        text: str = "",
        command: Optional[Callable[[], None]] = None,
        radius: int = 14,
        bg_color: str = "#1f1b34",
        fg_color: str = "#f1f5f9",
        hover_bg: str = "#2b2647",
        hover_fg: str = "#ffffff",
        active_bg: Optional[str] = None,
        border_color: str = "",
        font: Any = ("Segoe UI", 12, "bold"),
        tooltip_text: str = "",
        **kwargs,
    ):
        super().__init__(
            master,
            highlightthickness=0,
            borderwidth=0,
            bg=master.cget("bg"),
            **kwargs,
        )
        self.text = text
        self.command = command
        self.radius = radius
        self.normal_bg = bg_color
        self.normal_fg = fg_color
        self.hover_bg = hover_bg
        self.hover_fg = hover_fg
        self.active_bg = active_bg or hover_bg
        self.border_color = border_color
        self.button_font = font

        self.is_hovered = False
        self.is_pressed = False
        self.tooltip = Tooltip(self, tooltip_text) if tooltip_text else None

        self.bind("<Configure>", self._redraw)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def set_colors(
        self,
        parent_bg: str,
        bg_color: str,
        fg_color: str,
        hover_bg: str,
        hover_fg: str,
        border_color: str = "",
        active_bg: Optional[str] = None,
    ) -> None:
        """Update button color scheme during theme transitions."""
        self.config(bg=parent_bg)
        self.normal_bg = bg_color
        self.normal_fg = fg_color
        self.hover_bg = hover_bg
        self.hover_fg = hover_fg
        self.border_color = border_color
        self.active_bg = active_bg or hover_bg
        if self.tooltip:
            self.tooltip.set_colors(bg_color, fg_color, border_color or hover_bg)
        self._redraw()

    def set_text(self, text: str) -> None:
        self.text = text
        self._redraw()

    def _redraw(self, event=None) -> None:
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()

        if w < 4 or h < 4:
            return

        # Determine current color state
        if self.is_pressed:
            fill_col = self.active_bg
            fg_col = self.hover_fg
            offset_y = 1
        elif self.is_hovered:
            fill_col = self.hover_bg
            fg_col = self.hover_fg
            offset_y = 0
        else:
            fill_col = self.normal_bg
            fg_col = self.normal_fg
            offset_y = 0

        pad = 2
        # Draw border outline if configured
        if self.border_color:
            draw_rounded_rectangle(
                self,
                pad - 1,
                pad - 1,
                w - pad + 1,
                h - pad + 1,
                radius=self.radius,
                fill=self.border_color,
                outline="",
            )

        # Draw main button shape
        draw_rounded_rectangle(
            self,
            pad,
            pad,
            w - pad,
            h - pad,
            radius=self.radius,
            fill=fill_col,
            outline="",
        )

        # Draw label
        self.create_text(
            w // 2,
            h // 2 + offset_y,
            text=self.text,
            fill=fg_col,
            font=self.button_font,
            justify=tk.CENTER,
        )

    def _on_enter(self, event=None) -> None:
        self.is_hovered = True
        self._redraw()

    def _on_leave(self, event=None) -> None:
        self.is_hovered = False
        self.is_pressed = False
        self._redraw()

    def _on_press(self, event=None) -> None:
        self.is_pressed = True
        self._redraw()

    def _on_release(self, event=None) -> None:
        if self.is_pressed:
            self.is_pressed = False
            self._redraw()
            if self.command and self.is_hovered:
                self.command()


class CalculatorUI:
    """
    Main Calculator Application Window and UI Controller.
    Manages display, button inputs, keyboard shortcuts, history, and theme updates.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.engine = CalculatorEngine(angle_mode="DEG")
        self.theme_manager = ThemeManager()
        self.history_manager = HistoryManager()

        # State flags
        self.is_scientific = True
        self.show_history = False
        self.current_expression = ""
        self.display_value = "0"
        self.has_result_displayed = False
        self.buttons: List[ModernButton] = []

        self._init_window()
        self._create_widgets()
        self._bind_keyboard()
        self.apply_theme(self.theme_manager.current)
        self.theme_manager.add_listener(self.apply_theme)
        self.history_manager.add_listener(self._on_history_updated)
        self._on_history_updated(self.history_manager.get_entries())

    def _init_window(self) -> None:
        self.root.title("QuantumCalc • Advanced Scientific Calculator")
        self.root.geometry("740x650")
        self.root.minsize(420, 520)

        # Configure root grid weights for dynamic resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Set application icon if present
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "calculator_icon.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

    def _create_widgets(self) -> None:
        theme = self.theme_manager.current

        # Main application frame
        self.main_container = tk.Frame(self.root, bg=theme["bg_app"])
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.columnconfigure(1, weight=0)  # History drawer
        self.main_container.rowconfigure(0, weight=1)

        # Left / Calculator Core Frame
        self.calc_frame = tk.Frame(self.main_container, bg=theme["bg_app"], padx=14, pady=12)
        self.calc_frame.grid(row=0, column=0, sticky="nsew")
        self.calc_frame.columnconfigure(0, weight=1)

        # 1. Top Control Bar (Mode toggle, DEG/RAD, Theme switch, History toggle)
        self._create_header_bar()

        # 2. Display Card
        self._create_display()

        # 3. Memory Bar
        self._create_memory_bar()

        # 4. Keypad Container (Scientific + Standard grids)
        self._create_keypad()

        # 5. Right History Drawer Frame (Collapsible)
        self._create_history_drawer()

    # ----------------- UI Builders -----------------

    def _create_header_bar(self) -> None:
        theme = self.theme_manager.current
        self.header_frame = tk.Frame(self.calc_frame, bg=theme["bg_app"])
        self.header_frame.pack(fill=tk.X, pady=(0, 8))

        # Brand / Title Label
        self.brand_label = tk.Label(
            self.header_frame,
            text="QUANTUM•CALC",
            font=("Segoe UI", 11, "bold"),
            bg=theme["bg_app"],
            fg=theme["accent_primary"],
        )
        self.brand_label.pack(side=tk.LEFT)

        # Memory Indicator Tag
        self.mem_badge = tk.Label(
            self.header_frame,
            text="[ M ]",
            font=("Segoe UI", 9, "bold"),
            bg=theme["bg_app"],
            fg=theme["fg_muted"],
        )
        self.mem_badge.pack(side=tk.LEFT, padx=(8, 0))

        # Angle mode indicator & toggle
        self.angle_btn = ModernButton(
            self.header_frame,
            text=f"📐 {self.engine.angle_mode}",
            command=self.toggle_angle_mode,
            radius=10,
            bg_color=theme["btn_sci_bg"],
            fg_color=theme["btn_sci_fg"],
            hover_bg=theme["btn_sci_hover"],
            hover_fg=theme["fg_text"],
            font=("Segoe UI", 9, "bold"),
            width=70,
            height=26,
            tooltip_text="Toggle Trigonometric Angle Mode (Degrees / Radians)",
        )
        self.angle_btn.pack(side=tk.RIGHT, padx=4)
        self.buttons.append(self.angle_btn)

        # History Toggle Button
        self.history_toggle_btn = ModernButton(
            self.header_frame,
            text="🕒 History",
            command=self.toggle_history,
            radius=10,
            bg_color=theme["btn_sci_bg"],
            fg_color=theme["btn_sci_fg"],
            hover_bg=theme["btn_sci_hover"],
            hover_fg=theme["fg_text"],
            font=("Segoe UI", 9, "bold"),
            width=80,
            height=26,
            tooltip_text="Toggle Calculation History (Ctrl+H)",
        )
        self.history_toggle_btn.pack(side=tk.RIGHT, padx=4)
        self.buttons.append(self.history_toggle_btn)

        # Theme Selector Button
        self.theme_btn = ModernButton(
            self.header_frame,
            text=f"{self.theme_manager.current_icon} Theme",
            command=self.cycle_theme,
            radius=10,
            bg_color=theme["btn_sci_bg"],
            fg_color=theme["btn_sci_fg"],
            hover_bg=theme["btn_sci_hover"],
            hover_fg=theme["fg_text"],
            font=("Segoe UI", 9, "bold"),
            width=84,
            height=26,
            tooltip_text="Cycle Visual Theme (Ctrl+T)",
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=4)
        self.buttons.append(self.theme_btn)

        # Scientific Mode Toggle
        self.mode_toggle_btn = ModernButton(
            self.header_frame,
            text="🔬 Scientific",
            command=self.toggle_mode,
            radius=10,
            bg_color=theme["btn_op_bg"],
            fg_color=theme["btn_op_fg"],
            hover_bg=theme["btn_op_hover"],
            hover_fg=theme["fg_text"],
            font=("Segoe UI", 9, "bold"),
            width=90,
            height=26,
            tooltip_text="Toggle Standard / Scientific Mode (Ctrl+S)",
        )
        self.mode_toggle_btn.pack(side=tk.RIGHT, padx=4)
        self.buttons.append(self.mode_toggle_btn)

    def _create_display(self) -> None:
        theme = self.theme_manager.current

        # Outer card frame
        self.display_card = tk.Frame(
            self.calc_frame,
            bg=theme["bg_display"],
            highlightbackground=theme["border_color"],
            highlightthickness=1,
            padx=16,
            pady=12,
        )
        self.display_card.pack(fill=tk.X, pady=(0, 10))

        # Secondary expression label (shows formula / previous calculation)
        self.expr_label = tk.Label(
            self.display_card,
            text="",
            font=("Segoe UI", 12),
            bg=theme["bg_display"],
            fg=theme["fg_muted"],
            anchor="e",
        )
        self.expr_label.pack(fill=tk.X)

        # Primary calculation & result display
        self.result_label = tk.Label(
            self.display_card,
            text=self.display_value,
            font=("Segoe UI", 28, "bold"),
            bg=theme["bg_display"],
            fg=theme["fg_text"],
            anchor="e",
        )
        self.result_label.pack(fill=tk.X, pady=(2, 0))

    def _create_memory_bar(self) -> None:
        theme = self.theme_manager.current
        self.memory_bar = tk.Frame(self.calc_frame, bg=theme["bg_app"])
        self.memory_bar.pack(fill=tk.X, pady=(0, 8))

        mem_items = [
            ("MC", self.mem_clear, "Memory Clear (Reset to 0)"),
            ("MR", self.mem_recall, "Memory Recall"),
            ("M+", self.mem_add, "Memory Add current value"),
            ("M-", self.mem_sub, "Memory Subtract current value"),
            ("MS", self.mem_store, "Memory Store current value"),
        ]

        for i, (label, cmd, tip) in enumerate(mem_items):
            self.memory_bar.columnconfigure(i, weight=1, uniform="mem")
            btn = ModernButton(
                self.memory_bar,
                text=label,
                command=cmd,
                radius=8,
                bg_color=theme["btn_mem_bg"],
                fg_color=theme["btn_mem_fg"],
                hover_bg=theme["btn_mem_hover"],
                hover_fg=theme["fg_text"],
                font=("Segoe UI", 10, "bold"),
                height=30,
                tooltip_text=tip,
            )
            btn.grid(row=0, column=i, padx=3, sticky="nsew")
            self.buttons.append(btn)

    def _create_keypad(self) -> None:
        theme = self.theme_manager.current

        self.keypad_container = tk.Frame(self.calc_frame, bg=theme["bg_app"])
        self.keypad_container.pack(fill=tk.BOTH, expand=True)

        self.keypad_container.rowconfigure(0, weight=1)
        self.keypad_container.columnconfigure(0, weight=3)  # Scientific side
        self.keypad_container.columnconfigure(1, weight=4)  # Standard side

        # Scientific keypad (3 columns x 5 rows)
        self.sci_frame = tk.Frame(self.keypad_container, bg=theme["bg_app"])
        self.sci_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        for c in range(3):
            self.sci_frame.columnconfigure(c, weight=1, uniform="sci_col")
        for r in range(5):
            self.sci_frame.rowconfigure(r, weight=1, uniform="sci_row")

        sci_buttons = [
            # Row 0
            ("sin", lambda: self.append_func("sin"), "Sine function", 0, 0),
            ("cos", lambda: self.append_func("cos"), "Cosine function", 0, 1),
            ("tan", lambda: self.append_func("tan"), "Tangent function", 0, 2),
            # Row 1
            ("asin", lambda: self.append_func("asin"), "Inverse Sine", 1, 0),
            ("acos", lambda: self.append_func("acos"), "Inverse Cosine", 1, 1),
            ("atan", lambda: self.append_func("atan"), "Inverse Tangent", 1, 2),
            # Row 2
            ("√x", lambda: self.append_func("sqrt"), "Square Root", 2, 0),
            ("x²", self.apply_square, "Square (x²)", 2, 1),
            ("x³", self.apply_cube, "Cube (x³)", 2, 2),
            # Row 3
            ("xʸ", lambda: self.append_token("^"), "Power (x^y)", 3, 0),
            ("log", lambda: self.append_func("log"), "Common Logarithm (base 10)", 3, 1),
            ("ln", lambda: self.append_func("ln"), "Natural Logarithm (base e)", 3, 2),
            # Row 4
            ("n!", lambda: self.append_token("!"), "Factorial (n!)", 4, 0),
            ("|x|", lambda: self.append_func("abs"), "Absolute Value", 4, 1),
            ("π", lambda: self.append_token("π"), "Pi Constant (3.14159...)", 4, 2),
        ]

        for text, cmd, tip, r, c in sci_buttons:
            btn = ModernButton(
                self.sci_frame,
                text=text,
                command=cmd,
                radius=12,
                bg_color=theme["btn_sci_bg"],
                fg_color=theme["btn_sci_fg"],
                hover_bg=theme["btn_sci_hover"],
                hover_fg=theme["fg_text"],
                border_color=theme["border_color"],
                font=("Segoe UI", 11, "bold"),
                tooltip_text=tip,
            )
            btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
            self.buttons.append(btn)

        # Standard keypad (4 columns x 5 rows)
        self.std_frame = tk.Frame(self.keypad_container, bg=theme["bg_app"])
        self.std_frame.grid(row=0, column=1, sticky="nsew")

        for c in range(4):
            self.std_frame.columnconfigure(c, weight=1, uniform="std_col")
        for r in range(5):
            self.std_frame.rowconfigure(r, weight=1, uniform="std_row")

        std_buttons = [
            # Row 0: Actions & High Level
            ("AC", self.clear_all, "Clear All (Esc)", 0, 0, "action"),
            ("DEL", self.delete_char, "Delete Last Character (Backspace)", 0, 1, "action"),
            ("%", lambda: self.append_token("%"), "Percentage / Modulo", 0, 2, "op"),
            ("÷", lambda: self.append_token("÷"), "Division (/)", 0, 3, "op"),
            # Row 1: 7 8 9 ×
            ("7", lambda: self.append_token("7"), "", 1, 0, "num"),
            ("8", lambda: self.append_token("8"), "", 1, 1, "num"),
            ("9", lambda: self.append_token("9"), "", 1, 2, "num"),
            ("×", lambda: self.append_token("×"), "Multiplication (*)", 1, 3, "op"),
            # Row 2: 4 5 6 −
            ("4", lambda: self.append_token("4"), "", 2, 0, "num"),
            ("5", lambda: self.append_token("5"), "", 2, 1, "num"),
            ("6", lambda: self.append_token("6"), "", 2, 2, "num"),
            ("−", lambda: self.append_token("-"), "Subtraction (-)", 2, 3, "op"),
            # Row 3: 1 2 3 +
            ("1", lambda: self.append_token("1"), "", 3, 0, "num"),
            ("2", lambda: self.append_token("2"), "", 3, 1, "num"),
            ("3", lambda: self.append_token("3"), "", 3, 2, "num"),
            ("+", lambda: self.append_token("+"), "Addition (+)", 3, 3, "op"),
            # Row 4: ± 0 . =
            ("±", self.toggle_sign, "Positive / Negative Toggle", 4, 0, "num"),
            ("0", lambda: self.append_token("0"), "", 4, 1, "num"),
            (".", lambda: self.append_token("."), "Decimal point", 4, 2, "num"),
            ("=", self.calculate_result, "Calculate Result (Enter)", 4, 3, "equal"),
        ]

        for text, cmd, tip, r, c, btype in std_buttons:
            if btype == "action":
                bg = theme["btn_action_bg"]
                fg = theme["btn_action_fg"]
                hover = theme["btn_action_hover"]
            elif btype == "op":
                bg = theme["btn_op_bg"]
                fg = theme["btn_op_fg"]
                hover = theme["btn_op_hover"]
            elif btype == "equal":
                bg = theme["btn_equal_bg"]
                fg = theme["btn_equal_fg"]
                hover = theme["btn_equal_hover"]
            else:
                bg = theme["btn_num_bg"]
                fg = theme["btn_num_fg"]
                hover = theme["btn_num_hover"]

            btn = ModernButton(
                self.std_frame,
                text=text,
                command=cmd,
                radius=12,
                bg_color=bg,
                fg_color=fg,
                hover_bg=hover,
                hover_fg=theme["fg_text"],
                border_color=theme["border_color"] if btype != "equal" else "",
                font=("Segoe UI", 13, "bold"),
                tooltip_text=tip,
            )
            btn.btype = btype  # tag for theming
            btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
            self.buttons.append(btn)

    def _create_history_drawer(self) -> None:
        theme = self.theme_manager.current

        self.history_drawer = tk.Frame(
            self.main_container,
            bg=theme["history_bg"],
            width=260,
            highlightbackground=theme["border_color"],
            highlightthickness=1,
            padx=10,
            pady=12,
        )
        # History is hidden by default
        self.history_drawer.grid_propagate(False)

        # Header with Title and Clear button
        head_frame = tk.Frame(self.history_drawer, bg=theme["history_bg"])
        head_frame.pack(fill=tk.X, pady=(0, 10))

        title = tk.Label(
            head_frame,
            text="History",
            font=("Segoe UI", 12, "bold"),
            bg=theme["history_bg"],
            fg=theme["fg_text"],
        )
        title.pack(side=tk.LEFT)

        clear_btn = ModernButton(
            head_frame,
            text="🗑️ Clear",
            command=self.history_manager.clear,
            radius=8,
            bg_color=theme["btn_action_bg"],
            fg_color=theme["btn_action_fg"],
            hover_bg=theme["btn_action_hover"],
            hover_fg=theme["fg_text"],
            font=("Segoe UI", 8, "bold"),
            width=65,
            height=24,
            tooltip_text="Clear calculation history",
        )
        clear_btn.pack(side=tk.RIGHT)
        self.buttons.append(clear_btn)

        # Scrollable container for history items
        self.history_canvas = tk.Canvas(
            self.history_drawer,
            bg=theme["history_bg"],
            highlightthickness=0,
            borderwidth=0,
        )
        self.history_scrollbar = tk.Scrollbar(
            self.history_drawer,
            orient="vertical",
            command=self.history_canvas.yview,
        )
        self.history_canvas.configure(yscrollcommand=self.history_scrollbar.set)

        self.history_items_frame = tk.Frame(self.history_canvas, bg=theme["history_bg"])
        self.history_window_id = self.history_canvas.create_window(
            (0, 0),
            window=self.history_items_frame,
            anchor="nw",
        )

        self.history_items_frame.bind(
            "<Configure>",
            lambda e: self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all")),
        )
        self.history_canvas.bind(
            "<Configure>",
            lambda e: self.history_canvas.itemconfig(self.history_window_id, width=e.width),
        )

        self.history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # ----------------- Keyboard Bindings -----------------

    def _bind_keyboard(self) -> None:
        """Bind complete keyboard interaction."""
        # Numbers 0-9
        for num in range(10):
            self.root.bind(str(num), lambda e, n=num: self.append_token(str(n)))
            self.root.bind(f"<KP_{num}>", lambda e, n=num: self.append_token(str(n)))

        # Operators
        self.root.bind("+", lambda e: self.append_token("+"))
        self.root.bind("<KP_Add>", lambda e: self.append_token("+"))
        self.root.bind("-", lambda e: self.append_token("-"))
        self.root.bind("<KP_Subtract>", lambda e: self.append_token("-"))
        self.root.bind("*", lambda e: self.append_token("×"))
        self.root.bind("<KP_Multiply>", lambda e: self.append_token("×"))
        self.root.bind("/", lambda e: self.append_token("÷"))
        self.root.bind("<KP_Divide>", lambda e: self.append_token("÷"))
        self.root.bind(".", lambda e: self.append_token("."))
        self.root.bind("<KP_Decimal>", lambda e: self.append_token("."))
        self.root.bind("%", lambda e: self.append_token("%"))
        self.root.bind("(", lambda e: self.append_token("("))
        self.root.bind(")", lambda e: self.append_token(")"))
        self.root.bind("^", lambda e: self.append_token("^"))
        self.root.bind("!", lambda e: self.append_token("!"))

        # Calculations & Clears
        self.root.bind("<Return>", lambda e: self.calculate_result())
        self.root.bind("<KP_Enter>", lambda e: self.calculate_result())
        self.root.bind("=", lambda e: self.calculate_result())
        self.root.bind("<BackSpace>", lambda e: self.delete_char())
        self.root.bind("<Escape>", lambda e: self.clear_all())
        self.root.bind("<Delete>", lambda e: self.clear_all())

        # Shortcuts
        self.root.bind("<Control-s>", lambda e: self.toggle_mode())
        self.root.bind("<Control-S>", lambda e: self.toggle_mode())
        self.root.bind("<Control-h>", lambda e: self.toggle_history())
        self.root.bind("<Control-H>", lambda e: self.toggle_history())
        self.root.bind("<Control-t>", lambda e: self.cycle_theme())
        self.root.bind("<Control-T>", lambda e: self.cycle_theme())
        self.root.bind("<Control-r>", lambda e: self.toggle_angle_mode())
        self.root.bind("<Control-R>", lambda e: self.toggle_angle_mode())

    # ----------------- Calculator Actions -----------------

    def append_token(self, token: str) -> None:
        """Append a number or operator token to expression."""
        if self.has_result_displayed and token in "0123456789.πe":
            # Start fresh after calculation if typing a new number
            self.current_expression = ""
            self.has_result_displayed = False
        elif self.has_result_displayed:
            # Continue calculating on top of last result
            self.has_result_displayed = False

        self.current_expression += token
        self._update_display(self.current_expression)

    def append_func(self, func_name: str) -> None:
        """Append a scientific function call e.g. sin( """
        if self.has_result_displayed:
            # Wrap previous result: sin(ans)
            self.current_expression = f"{func_name}({self.current_expression})"
            self.has_result_displayed = False
        else:
            self.current_expression += f"{func_name}("
        self._update_display(self.current_expression)

    def apply_square(self) -> None:
        """Apply square operation x²."""
        if not self.current_expression:
            return
        self.current_expression = f"({self.current_expression})^2"
        self._update_display(self.current_expression)

    def apply_cube(self) -> None:
        """Apply cube operation x³."""
        if not self.current_expression:
            return
        self.current_expression = f"({self.current_expression})^3"
        self._update_display(self.current_expression)

    def toggle_sign(self) -> None:
        """Toggle positive/negative sign of current expression or number."""
        if not self.current_expression or self.current_expression == "0":
            return
        if self.current_expression.startswith("-(") and self.current_expression.endswith(")"):
            self.current_expression = self.current_expression[2:-1]
        elif self.current_expression.startswith("-"):
            self.current_expression = self.current_expression[1:]
        else:
            self.current_expression = f"-({self.current_expression})"
        self._update_display(self.current_expression)

    def delete_char(self) -> None:
        """Backspace / delete last character."""
        if self.has_result_displayed:
            self.clear_all()
            return
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]
            self._update_display(self.current_expression if self.current_expression else "0")

    def clear_all(self) -> None:
        """AC - clear everything."""
        self.current_expression = ""
        self.has_result_displayed = False
        self.expr_label.config(text="")
        self._update_display("0")

    def calculate_result(self) -> None:
        """Evaluate expression and display formatted result."""
        if not self.current_expression.strip():
            return

        raw_expr = self.current_expression
        ok, res = self.engine.evaluate(raw_expr)

        if ok:
            formatted = self.engine.format_result(res)
            # Display prior expression above result
            self.expr_label.config(text=f"{raw_expr} =")
            self._update_display(formatted, is_result=True)
            self.history_manager.add_entry(raw_expr, formatted)
            self.current_expression = str(formatted).replace(" ", "")
            self.has_result_displayed = True
        else:
            # Display error message cleanly
            self.expr_label.config(text=f"{raw_expr} =")
            self._show_error(str(res))
            self.has_result_displayed = True

    def _update_display(self, text: str, is_result: bool = False) -> None:
        theme = self.theme_manager.current
        self.display_value = text
        self.result_label.config(
            text=text,
            fg=theme["accent_secondary"] if is_result else theme["fg_text"],
        )

    def _show_error(self, message: str) -> None:
        theme = self.theme_manager.current
        self.result_label.config(
            text=message,
            fg=theme["btn_action_fg"],
        )

    # ----------------- Memory Actions -----------------

    def _get_current_numeric_val(self) -> float:
        try:
            ok, res = self.engine.evaluate(self.current_expression if self.current_expression else "0")
            return float(res) if ok else 0.0
        except Exception:
            return 0.0

    def mem_clear(self) -> None:
        self.engine.memory_clear()
        self._update_mem_badge()

    def mem_recall(self) -> None:
        val = self.engine.memory_recall()
        formatted = self.engine.format_result(val)
        self.append_token(str(formatted))
        self._update_mem_badge()

    def mem_add(self) -> None:
        val = self._get_current_numeric_val()
        self.engine.memory_add(val)
        self._update_mem_badge()

    def mem_sub(self) -> None:
        val = self._get_current_numeric_val()
        self.engine.memory_subtract(val)
        self._update_mem_badge()

    def mem_store(self) -> None:
        val = self._get_current_numeric_val()
        self.engine.memory_store(val)
        self._update_mem_badge()

    def _update_mem_badge(self) -> None:
        theme = self.theme_manager.current
        if self.engine.has_memory():
            self.mem_badge.config(fg=theme["accent_primary"], text=f"[ M: {self.engine.format_result(self.engine.memory)} ]")
        else:
            self.mem_badge.config(fg=theme["fg_muted"], text="[ M ]")

    # ----------------- Mode & Themes -----------------

    def toggle_mode(self) -> None:
        """Toggle between Standard and Scientific modes."""
        self.is_scientific = not self.is_scientific
        if self.is_scientific:
            self.sci_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
            self.mode_toggle_btn.set_text("🔬 Scientific")
            self.keypad_container.columnconfigure(0, weight=3)
        else:
            self.sci_frame.grid_remove()
            self.mode_toggle_btn.set_text("🔢 Standard")
            self.keypad_container.columnconfigure(0, weight=0)

    def toggle_angle_mode(self) -> None:
        mode = self.engine.toggle_angle_mode()
        self.angle_btn.set_text(f"📐 {mode}")

    def toggle_history(self) -> None:
        """Toggle history drawer visibility."""
        self.show_history = not self.show_history
        if self.show_history:
            self.history_drawer.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
            self.history_toggle_btn.set_text("✕ Close")
        else:
            self.history_drawer.grid_remove()
            self.history_toggle_btn.set_text("🕒 History")

    def cycle_theme(self) -> None:
        self.theme_manager.cycle_theme()

    def apply_theme(self, theme: Dict[str, str]) -> None:
        """Apply the current theme palette across all UI widgets."""
        bg_app = theme["bg_app"]
        self.root.config(bg=bg_app)
        self.main_container.config(bg=bg_app)
        self.calc_frame.config(bg=bg_app)
        self.header_frame.config(bg=bg_app)
        self.brand_label.config(bg=bg_app, fg=theme["accent_primary"])
        self.memory_bar.config(bg=bg_app)
        self.keypad_container.config(bg=bg_app)
        self.sci_frame.config(bg=bg_app)
        self.std_frame.config(bg=bg_app)

        # Update display card
        self.display_card.config(
            bg=theme["bg_display"],
            highlightbackground=theme["border_color"],
        )
        self.expr_label.config(bg=theme["bg_display"], fg=theme["fg_muted"])
        self.result_label.config(bg=theme["bg_display"], fg=theme["fg_text"])
        self._update_mem_badge()

        # Update theme selector button icon
        self.theme_btn.set_text(f"{self.theme_manager.current_icon} Theme")

        # Update History drawer
        self.history_drawer.config(
            bg=theme["history_bg"],
            highlightbackground=theme["border_color"],
        )
        self.history_canvas.config(bg=theme["history_bg"])
        self.history_items_frame.config(bg=theme["history_bg"])

        # Update all modern buttons
        for btn in self.buttons:
            if hasattr(btn, "btype"):
                btype = btn.btype
                if btype == "action":
                    bg = theme["btn_action_bg"]
                    fg = theme["btn_action_fg"]
                    hbg = theme["btn_action_hover"]
                elif btype == "op":
                    bg = theme["btn_op_bg"]
                    fg = theme["btn_op_fg"]
                    hbg = theme["btn_op_hover"]
                elif btype == "equal":
                    bg = theme["btn_equal_bg"]
                    fg = theme["btn_equal_fg"]
                    hbg = theme["btn_equal_hover"]
                else:
                    bg = theme["btn_num_bg"]
                    fg = theme["btn_num_fg"]
                    hbg = theme["btn_num_hover"]
                btn.set_colors(
                    parent_bg=bg_app,
                    bg_color=bg,
                    fg_color=fg,
                    hover_bg=hbg,
                    hover_fg=theme["fg_text"],
                    border_color=theme["border_color"] if btype != "equal" else "",
                )
            else:
                # Header / Utility buttons
                btn.set_colors(
                    parent_bg=bg_app,
                    bg_color=theme["btn_sci_bg"],
                    fg_color=theme["btn_sci_fg"],
                    hover_bg=theme["btn_sci_hover"],
                    hover_fg=theme["fg_text"],
                    border_color=theme["border_color"],
                )

        self._refresh_history_cards()

    # ----------------- History View -----------------

    def _on_history_updated(self, entries: List[Dict[str, Any]]) -> None:
        self._refresh_history_cards()

    def _refresh_history_cards(self) -> None:
        """Render recent history calculations inside drawer."""
        theme = self.theme_manager.current

        # Clear existing history widgets
        for child in self.history_items_frame.winfo_children():
            child.destroy()

        entries = self.history_manager.get_entries()
        if not entries:
            empty_lbl = tk.Label(
                self.history_items_frame,
                text="No calculations yet.\nStart calculating to see\nyour history here.",
                font=("Segoe UI", 9),
                bg=theme["history_bg"],
                fg=theme["fg_muted"],
                justify=tk.CENTER,
                pady=24,
            )
            empty_lbl.pack(fill=tk.X)
            return

        for entry in entries:
            card = tk.Frame(
                self.history_items_frame,
                bg=theme["history_card_bg"],
                highlightbackground=theme["border_color"],
                highlightthickness=1,
                padx=10,
                pady=6,
                cursor="hand2",
            )
            card.pack(fill=tk.X, pady=3, padx=2)

            time_lbl = tk.Label(
                card,
                text=entry.get("timestamp", ""),
                font=("Segoe UI", 8),
                bg=theme["history_card_bg"],
                fg=theme["fg_muted"],
                anchor="w",
            )
            time_lbl.pack(fill=tk.X)

            expr_lbl = tk.Label(
                card,
                text=entry.get("expression", ""),
                font=("Segoe UI", 10),
                bg=theme["history_card_bg"],
                fg=theme["fg_text"],
                anchor="w",
                wraplength=210,
                justify=tk.LEFT,
            )
            expr_lbl.pack(fill=tk.X)

            res_lbl = tk.Label(
                card,
                text=f"= {entry.get('result', '')}",
                font=("Segoe UI", 11, "bold"),
                bg=theme["history_card_bg"],
                fg=theme["accent_primary"],
                anchor="e",
            )
            res_lbl.pack(fill=tk.X)

            # Click card to load result / expression
            def on_card_click(e, expr=entry.get("expression", ""), res=entry.get("result", "")):
                self.current_expression = res.replace(" ", "")
                self.expr_label.config(text=f"Loaded: {expr}")
                self._update_display(res, is_result=True)
                self.has_result_displayed = True

            def on_enter(e, c=card):
                c.config(bg=theme["history_card_hover"])
                for child in c.winfo_children():
                    child.config(bg=theme["history_card_hover"])

            def on_leave(e, c=card):
                c.config(bg=theme["history_card_bg"])
                for child in c.winfo_children():
                    child.config(bg=theme["history_card_bg"])

            for widget in (card, time_lbl, expr_lbl, res_lbl):
                widget.bind("<Button-1>", on_card_click)
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
