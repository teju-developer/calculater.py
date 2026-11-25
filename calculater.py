
import tkinter as tk
import ast
import math
import operator


# ==========================================
# SAFE MATHEMATICAL CALCULATOR ENGINE
# ==========================================

class SafeCalculator:

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    UNARY_OPERATORS = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def __init__(self, degrees=True):
        self.degrees = degrees

    def functions(self):

        if self.degrees:
            sin = lambda x: math.sin(math.radians(x))
            cos = lambda x: math.cos(math.radians(x))
            tan = lambda x: math.tan(math.radians(x))
            asin = lambda x: math.degrees(math.asin(x))
            acos = lambda x: math.degrees(math.acos(x))
            atan = lambda x: math.degrees(math.atan(x))
        else:
            sin = math.sin
            cos = math.cos
            tan = math.tan
            asin = math.asin
            acos = math.acos
            atan = math.atan

        return {
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "asin": asin,
            "acos": acos,
            "atan": atan,
            "sqrt": math.sqrt,
            "log": math.log10,
            "ln": math.log,
            "factorial": math.factorial,
            "abs": abs,
            "exp": math.exp,
        }

    def evaluate_node(self, node):

        if isinstance(node, ast.Expression):
            return self.evaluate_node(node.body)

        if isinstance(node, ast.Constant):

            if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                return node.value

            raise ValueError("Invalid number")

        if isinstance(node, ast.Name):

            constants = {
                "pi": math.pi,
                "e": math.e
            }

            if node.id in constants:
                return constants[node.id]

            raise ValueError("Unknown constant")

        if isinstance(node, ast.BinOp):

            operation = self.OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operation")

            left = self.evaluate_node(node.left)
            right = self.evaluate_node(node.right)

            if isinstance(node.op, ast.Div) and right == 0:
                raise ZeroDivisionError

            if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                raise ValueError("Exponent too large")

            result = operation(left, right)

            return self.validate_result(result)

        if isinstance(node, ast.UnaryOp):

            operation = self.UNARY_OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Invalid unary operation")

            result = operation(self.evaluate_node(node.operand))

            return self.validate_result(result)

        if isinstance(node, ast.Call):

            if not isinstance(node.func, ast.Name):
                raise ValueError("Invalid function")

            function = self.functions().get(node.func.id)

            if function is None or node.keywords or len(node.args) != 1:
                raise ValueError("Unsupported function")

            argument = self.evaluate_node(node.args[0])

            if node.func.id == "factorial":

                if not isinstance(argument, int) or argument < 0 or argument > 170:
                    raise ValueError("Factorial requires an integer from 0 to 170")

            return self.validate_result(function(argument))

        raise ValueError("Invalid expression")

    @staticmethod
    def validate_result(value):

        if isinstance(value, complex):
            raise ValueError("Complex results are not supported")

        if not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError("Result is out of range")

        return value

    def calculate(self, expression):

        if not expression.strip():
            raise ValueError("Enter an expression")

        tree = ast.parse(expression, mode="eval")

        if sum(1 for _ in ast.walk(tree)) > 100:
            raise ValueError("Expression is too long")

        return self.evaluate_node(tree)


# ==========================================
# MAIN CALCULATOR APPLICATION
# ==========================================

class CalculatorApp:

    BG = "#10141D"
    DISPLAY_BG = "#1A2230"
    NUMBER_BG = "#263244"
    OPERATOR_BG = "#344B68"
    SCI_BG = "#253B50"
    ACCENT = "#08B9A6"
    TEXT = "#F4F7FB"
    MUTED = "#A8B5C7"

    def __init__(self, root):

        self.root = root

        self.root.title("NovaCalc | Scientific Calculator")
        self.root.geometry("480x700")
        self.root.minsize(370, 560)
        self.root.configure(bg=self.BG)

        self.expression = tk.StringVar()
        self.result_text = tk.StringVar(value="= 0")

        self.degrees = True
        self.scientific_visible = True

        self.calculator = SafeCalculator(self.degrees)
        self.history = []

        self.create_interface()
        self.bind_keyboard()

    # ======================================
    # CREATE GUI
    # ======================================

    def create_interface(self):

        header = tk.Frame(self.root, bg=self.BG)
        header.pack(fill="x", padx=18, pady=(16, 8))

        tk.Label(
            header,
            text="NOVACALC",
            font=("Segoe UI", 18, "bold"),
            bg=self.BG,
            fg=self.ACCENT
        ).pack(side="left")

        tk.Button(
            header,
            text="History",
            command=self.show_history,
            bg=self.DISPLAY_BG,
            fg=self.TEXT,
            activebackground=self.OPERATOR_BG,
            activeforeground=self.TEXT,
            relief="flat",
            padx=12,
            pady=7,
            cursor="hand2"
        ).pack(side="right")

        # Display section

        display = tk.Frame(
            self.root,
            bg=self.DISPLAY_BG,
            highlightthickness=1,
            highlightbackground="#334155"
        )

        display.pack(fill="x", padx=18, pady=10)

        self.display_entry = tk.Entry(
            display,
            textvariable=self.expression,
            font=("Segoe UI", 25),
            bg=self.DISPLAY_BG,
            fg=self.TEXT,
            insertbackground=self.ACCENT,
            justify="right",
            relief="flat",
            bd=0
        )

        self.display_entry.pack(
            fill="x",
            padx=15,
            pady=(20, 8),
            ipady=8
        )

        tk.Label(
            display,
            textvariable=self.result_text,
            font=("Segoe UI", 17, "bold"),
            bg=self.DISPLAY_BG,
            fg=self.ACCENT,
            anchor="e"
        ).pack(fill="x", padx=16, pady=(0, 15))

        # Calculator controls

        controls = tk.Frame(self.root, bg=self.BG)
        controls.pack(fill="x", padx=18, pady=5)

        self.mode_button = tk.Button(
            controls,
            text="DEG",
            command=self.toggle_angle_mode,
            bg=self.SCI_BG,
            fg=self.ACCENT,
            activebackground=self.OPERATOR_BG,
            activeforeground=self.TEXT,
            relief="flat",
            padx=15,
            pady=7,
            cursor="hand2"
        )

        self.mode_button.pack(side="left")

        tk.Button(
            controls,
            text="Scientific ▼",
            command=self.toggle_scientific,
            bg=self.SCI_BG,
            fg=self.TEXT,
            activebackground=self.OPERATOR_BG,
            activeforeground=self.TEXT,
            relief="flat",
            padx=12,
            pady=7,
            cursor="hand2"
        ).pack(side="right")

        # Scientific buttons

        self.scientific_frame = tk.Frame(
            self.root,
            bg=self.BG
        )

        self.scientific_frame.pack(
            fill="x",
            padx=18,
            pady=(8, 4)
        )

        scientific_buttons = [
            ("sin", "sin("),
            ("cos", "cos("),
            ("tan", "tan("),
            ("√", "sqrt("),
            ("x²", "**2"),

            ("asin", "asin("),
            ("acos", "acos("),
            ("atan", "atan("),
            ("log", "log("),
            ("ln", "ln("),

            ("π", "pi"),
            ("e", "e"),
            ("!", "factorial("),
            ("(", "("),
            (")", ")"),

            ("xʸ", "**"),
            ("EXP", "exp("),
            ("ABS", "abs("),
            ("MOD", "%"),
            ("÷", "/")
        ]

        for index, (label, value) in enumerate(scientific_buttons):

            self.make_button(
                self.scientific_frame,
                label,
                lambda v=value: self.add_value(v),
                self.SCI_BG,
                index // 5,
                index % 5
            )

        # Main calculator buttons

        self.button_frame = tk.Frame(
            self.root,
            bg=self.BG
        )

        self.button_frame.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=8
        )

        buttons = [
            ("C", "clear", "clear"),
            ("⌫", "back", "back"),
            ("%", "percent", "operator"),
            ("÷", "/", "operator"),

            ("7", "7", "number"),
            ("8", "8", "number"),
            ("9", "9", "number"),
            ("×", "*", "operator"),

            ("4", "4", "number"),
            ("5", "5", "number"),
            ("6", "6", "number"),
            ("−", "-", "operator"),

            ("1", "1", "number"),
            ("2", "2", "number"),
            ("3", "3", "number"),
            ("+", "+", "operator"),

            ("±", "sign", "operator"),
            ("0", "0", "number"),
            (".", ".", "number"),
            ("=", "equals", "equals")
        ]

        colors = {
            "number": self.NUMBER_BG,
            "operator": self.OPERATOR_BG,
            "clear": "#8E3545",
            "back": "#624A36",
            "equals": self.ACCENT
        }

        for index, (label, value, kind) in enumerate(buttons):

            row, column = divmod(index, 4)

            self.make_button(
                self.button_frame,
                label,
                lambda v=value: self.button_action(v),
                colors[kind],
                row,
                column,
                bold=(kind == "equals")
            )

        for column in range(4):
            self.button_frame.grid_columnconfigure(column, weight=1)

        for row in range(5):
            self.button_frame.grid_rowconfigure(row, weight=1)

        # Footer

        tk.Label(
            self.root,
            text="Python • Tkinter • Scientific Calculator",
            font=("Segoe UI", 9),
            bg=self.BG,
            fg=self.MUTED
        ).pack(pady=(0, 10))

    # ======================================
    # BUTTON DESIGN
    # ======================================

    def make_button(
        self, parent, text, command,
        color, row, column, bold=False
    ):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=(
                "Segoe UI",
                12,
                "bold" if bold else "normal"
            ),
            bg=color,
            fg=self.TEXT,
            activebackground=self.ACCENT,
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=4,
            pady=9
        )

        button.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=4,
            pady=4
        )

        return button

    # ======================================
    # CALCULATOR OPERATIONS
    # ======================================

    def add_value(self, value):

        self.expression.set(
            self.expression.get() + value
        )

        self.result_text.set("")

        self.display_entry.icursor(tk.END)

    def button_action(self, value):

        if value == "clear":
            self.clear()

        elif value == "back":
            self.backspace()

        elif value == "equals":
            self.calculate()

        elif value == "sign":
            self.toggle_sign()

        elif value == "percent":
            self.apply_percent()

        else:
            self.add_value(value)

    def clear(self):

        self.expression.set("")
        self.result_text.set("= 0")

    def backspace(self):

        current = self.expression.get()

        if current:
            self.expression.set(current[:-1])

        self.result_text.set("")

    def toggle_sign(self):

        current = self.expression.get().strip()

        if not current:
            self.expression.set("-")

        elif current.startswith("-(") and current.endswith(")"):
            self.expression.set(current[2:-1])

        else:
            self.expression.set(f"-({current})")

        self.result_text.set("")

    def apply_percent(self):

        current = self.expression.get().strip()

        if current:
            self.expression.set(f"({current})/100")

        self.result_text.set("")

    # ======================================
    # CALCULATE RESULT
    # ======================================

    def calculate(self):

        expression = self.expression.get().strip()

        if not expression:
            return

        try:

            self.calculator.degrees = self.degrees

            result = self.calculator.calculate(expression)

            if isinstance(result, float):

                if result.is_integer():
                    result = int(result)

                else:
                    result = round(result, 12)

            result_string = str(result)

            self.history.append(
                f"{expression} = {result_string}"
            )

            # Show result with equals sign

            self.result_text.set(
                f"= {result_string}"
            )

        except ZeroDivisionError:

            self.result_text.set("Cannot divide by zero")

        except SyntaxError:

            self.result_text.set("Invalid expression")

        except (ValueError, OverflowError):

            self.result_text.set(
                "Invalid input or mathematical error"
            )

        except Exception:

            self.result_text.set(
                "Unable to calculate expression"
            )

    # ======================================
    # DEGREE / RADIAN MODE
    # ======================================

    def toggle_angle_mode(self):

        self.degrees = not self.degrees

        self.mode_button.config(
            text="DEG" if self.degrees else "RAD"
        )

        self.result_text.set(
            "Degree mode" if self.degrees else "Radian mode"
        )

    # ======================================
    # SCIENTIFIC MODE
    # ======================================

    def toggle_scientific(self):

        if self.scientific_visible:

            self.scientific_frame.pack_forget()
            self.scientific_visible = False

        else:

            self.scientific_frame.pack(
                fill="x",
                padx=18,
                pady=(8, 4),
                before=self.button_frame
            )

            self.scientific_visible = True

    # ======================================
    # CALCULATION HISTORY
    # ======================================

    def show_history(self):

        window = tk.Toplevel(self.root)

        window.title("Calculation History")
        window.geometry("400x450")
        window.configure(bg=self.BG)

        tk.Label(
            window,
            text="Calculation History",
            font=("Segoe UI", 17, "bold"),
            bg=self.BG,
            fg=self.ACCENT
        ).pack(pady=12)

        listbox = tk.Listbox(
            window,
            font=("Consolas", 11),
            bg=self.DISPLAY_BG,
            fg=self.TEXT,
            selectbackground=self.ACCENT,
            relief="flat"
        )

        listbox.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        for item in reversed(self.history):
            listbox.insert(tk.END, item)

        if not self.history:
            listbox.insert(tk.END, "No calculations yet.")

        tk.Button(
            window,
            text="Close",
            command=window.destroy,
            bg=self.ACCENT,
            fg="white",
            relief="flat",
            padx=20,
            pady=8
        ).pack(pady=12)

    # ======================================
    # KEYBOARD SUPPORT
    # ======================================

    def bind_keyboard(self):

        self.root.bind(
            "<Return>",
            lambda event: self.calculate()
        )

        self.root.bind(
            "<KP_Enter>",
            lambda event: self.calculate()
        )

        self.root.bind(
            "<Escape>",
            lambda event: self.clear()
        )

        # Avoid double deletion while typing in the Entry.

        self.display_entry.bind(
            "<BackSpace>",
            self.keyboard_backspace
        )

        self.display_entry.bind(
            "<Return>",
            self.keyboard_enter
        )

        self.display_entry.bind(
            "<KP_Enter>",
            self.keyboard_enter
        )

        self.display_entry.bind(
            "<Escape>",
            self.keyboard_escape
        )

    def keyboard_backspace(self, event):

        self.backspace()
        return "break"

    def keyboard_enter(self, event):

        self.calculate()
        return "break"

    def keyboard_escape(self, event):

        self.clear()
        return "break"


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CalculatorApp(root)

    root.mainloop()
