"""
Safe Mathematical Calculation Engine for Scientific Calculator.
Uses Python's AST (Abstract Syntax Tree) to parse and evaluate mathematical
expressions securely without arbitrary code execution.
"""

import ast
import math
import re
from typing import Any, Dict, Tuple, Union


class CalculationError(Exception):
    """Custom exception for calculation errors with user-friendly messages."""
    pass


class CalculatorEngine:
    """
    Secure mathematical engine supporting basic and scientific operations,
    degree/radian modes, memory functions, and friendly error reporting.
    """

    def __init__(self, angle_mode: str = "DEG"):
        """
        Initialize calculator engine.
        :param angle_mode: 'DEG' (degrees) or 'RAD' (radians)
        """
        self.angle_mode = angle_mode.upper() if angle_mode.upper() in ("DEG", "RAD") else "DEG"
        self.memory: float = 0.0
        self.last_result: Union[float, int, None] = None

    def set_angle_mode(self, mode: str) -> str:
        """Switch angle mode between DEG and RAD."""
        if mode.upper() in ("DEG", "RAD"):
            self.angle_mode = mode.upper()
        return self.angle_mode

    def toggle_angle_mode(self) -> str:
        """Toggle between DEG and RAD mode."""
        self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
        return self.angle_mode

    # ----------------- Memory Operations -----------------

    def memory_clear(self) -> None:
        """Clear memory (MC)."""
        self.memory = 0.0

    def memory_recall(self) -> float:
        """Recall stored memory (MR)."""
        return self.memory

    def memory_add(self, value: Union[int, float]) -> float:
        """Add value to memory (M+)."""
        self.memory += float(value)
        return self.memory

    def memory_subtract(self, value: Union[int, float]) -> float:
        """Subtract value from memory (M-)."""
        self.memory -= float(value)
        return self.memory

    def memory_store(self, value: Union[int, float]) -> float:
        """Store value in memory (MS)."""
        self.memory = float(value)
        return self.memory

    def has_memory(self) -> bool:
        """Check if memory contains a non-zero value."""
        return abs(self.memory) > 1e-15

    # ----------------- Math Helpers -----------------

    def _sin(self, x: float) -> float:
        if self.angle_mode == "DEG":
            # Exact zeroes for 180 multiples
            x_deg = x % 360
            if math.isclose(x_deg, 0, abs_tol=1e-12) or math.isclose(x_deg, 180, abs_tol=1e-12) or math.isclose(x_deg, 360, abs_tol=1e-12):
                return 0.0
            if math.isclose(x_deg, 90, abs_tol=1e-12):
                return 1.0
            if math.isclose(x_deg, 270, abs_tol=1e-12):
                return -1.0
            val = math.sin(math.radians(x))
        else:
            val = math.sin(x)
        return 0.0 if abs(val) < 1e-15 else val

    def _cos(self, x: float) -> float:
        if self.angle_mode == "DEG":
            x_deg = x % 360
            if math.isclose(x_deg, 90, abs_tol=1e-12) or math.isclose(x_deg, 270, abs_tol=1e-12):
                return 0.0
            if math.isclose(x_deg, 0, abs_tol=1e-12) or math.isclose(x_deg, 360, abs_tol=1e-12):
                return 1.0
            if math.isclose(x_deg, 180, abs_tol=1e-12):
                return -1.0
            val = math.cos(math.radians(x))
        else:
            val = math.cos(x)
        return 0.0 if abs(val) < 1e-15 else val

    def _tan(self, x: float) -> float:
        if self.angle_mode == "DEG":
            x_deg = abs(x) % 180
            if math.isclose(x_deg, 90, abs_tol=1e-9):
                raise CalculationError("Undefined (tan 90°)")
            val = math.tan(math.radians(x))
        else:
            if math.isclose(abs(x) % math.pi, math.pi / 2, abs_tol=1e-9):
                raise CalculationError("Undefined (tan π/2)")
            val = math.tan(x)
        return 0.0 if abs(val) < 1e-15 else val

    def _asin(self, x: float) -> float:
        if x < -1.0 or x > 1.0:
            raise CalculationError("Domain Error: asin requires -1 ≤ x ≤ 1")
        rad = math.asin(x)
        return math.degrees(rad) if self.angle_mode == "DEG" else rad

    def _acos(self, x: float) -> float:
        if x < -1.0 or x > 1.0:
            raise CalculationError("Domain Error: acos requires -1 ≤ x ≤ 1")
        rad = math.acos(x)
        return math.degrees(rad) if self.angle_mode == "DEG" else rad

    def _atan(self, x: float) -> float:
        rad = math.atan(x)
        return math.degrees(rad) if self.angle_mode == "DEG" else rad

    def _sqrt(self, x: float) -> float:
        if x < 0:
            raise CalculationError("Domain Error: Negative square root")
        return math.sqrt(x)

    def _cbrt(self, x: float) -> float:
        if x < 0:
            return -math.pow(-x, 1.0 / 3.0)
        return math.pow(x, 1.0 / 3.0)

    def _log10(self, x: float) -> float:
        if x <= 0:
            raise CalculationError("Domain Error: log requires x > 0")
        return math.log10(x)

    def _ln(self, x: float) -> float:
        if x <= 0:
            raise CalculationError("Domain Error: ln requires x > 0")
        return math.log(x)

    def _log2(self, x: float) -> float:
        if x <= 0:
            raise CalculationError("Domain Error: log2 requires x > 0")
        return math.log2(x)

    def _factorial(self, x: float) -> int:
        if x < 0:
            raise CalculationError("Factorial Error: Negative input")
        if not math.isclose(x, round(x), abs_tol=1e-9):
            raise CalculationError("Factorial Error: Non-integer input")
        n = int(round(x))
        if n > 170:
            raise CalculationError("Overflow: Factorial exceeds limit (n ≤ 170)")
        return math.factorial(n)

    def _power(self, base: float, exp: float) -> float:
        if abs(exp) > 10000:
            raise CalculationError("Overflow: Exponent too large")
        if base < 0 and not math.isclose(exp, round(exp), abs_tol=1e-9):
            raise CalculationError("Domain Error: Negative base with fractional exponent")
        try:
            res = base ** exp
            if isinstance(res, complex):
                raise CalculationError("Complex result not supported")
            return res
        except OverflowError:
            raise CalculationError("Overflow: Calculation result too large")

    # ----------------- Preprocessing -----------------

    def preprocess_expression(self, expr: str) -> str:
        """
        Clean and normalize expressions from user input into Python-syntax AST.
        """
        if not expr or not expr.strip():
            return ""

        s = expr.strip()

        # Unicode replacements
        s = s.replace("×", "*").replace("÷", "/").replace("−", "-")
        s = s.replace("–", "-").replace("·", "*")
        s = s.replace("π", "pi")

        # Scientific notation shorthand
        s = re.sub(r'\bAns\b', str(self.last_result if self.last_result is not None else 0), s, flags=re.IGNORECASE)

        # Handle power syntax x^y -> x**y
        s = s.replace("^", "**")

        # Percentage notation:
        # e.g., 50% -> (50/100)
        # 10 + 20% -> 10 + (20/100)
        s = re.sub(r'(\d+(?:\.\d+)?)%', r'(\1/100)', s)
        s = re.sub(r'\(([^()]+)\)%', r'((\1)/100)', s)

        # Factorial notation: 5! -> fact(5)
        # Repeatedly replace outermost/innermost n!
        for _ in range(3):
            s = re.sub(r'(\d+)!', r'fact(\1)', s)
            s = re.sub(r'\(([^()]+)\)!', r'fact(\1)', s)

        # Implicit multiplication:
        # 2(3) -> 2*(3) (but not log2(3))
        s = re.sub(r'(?<![a-zA-Z_])(\d+)\s*\(', r'\1*(', s)
        s = re.sub(r'\)\s*\(', r')*(', s)
        s = re.sub(r'\)\s*(\d+)', r')*\1', s)
        s = re.sub(r'(?<![a-zA-Z_])(\d+)\s*(pi|sin|cos|tan|asin|acos|atan|log|ln|sqrt|cbrt|abs|fact)', r'\1*\2', s)
        s = re.sub(r'\)\s*(pi|e|sin|cos|tan|asin|acos|atan|log|ln|sqrt|cbrt|abs|fact)', r')*\1', s)

        # Match numbers right next to 'e' that are NOT scientific notation (e.g. 5e where not followed by digit or sign)
        # e.g. 2*e or 3e+4
        s = re.sub(r'(?<![a-zA-Z_])(\d+)\s*e(?![0-9\+\-a-zA-Z_])', r'\1*e', s)

        return s

    # ----------------- AST Evaluator -----------------

    def _eval_node(self, node: ast.AST) -> float:
        """Recursively evaluate an AST node safely."""
        if isinstance(node, ast.Expression):
            return self._eval_node(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise CalculationError("Invalid constant type")

        # Compatibility with older AST representations
        if hasattr(ast, "Num") and isinstance(node, ast.Num):
            return float(node.n)

        if isinstance(node, ast.Name):
            name = node.id
            if name == "pi":
                return math.pi
            if name == "e":
                return math.e
            if name == "tau":
                return math.tau
            raise CalculationError(f"Unknown variable or identifier: '{name}'")

        if isinstance(node, ast.UnaryOp):
            val = self._eval_node(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +val
            if isinstance(node.op, ast.USub):
                return -val
            raise CalculationError(f"Unsupported unary operator: {type(node.op).__name__}")

        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)

            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                if right == 0:
                    raise CalculationError("Cannot divide by zero")
                return left / right
            if isinstance(node.op, ast.Mod):
                if right == 0:
                    raise CalculationError("Modulo by zero")
                return left % right
            if isinstance(node.op, ast.Pow):
                return self._power(left, right)
            if isinstance(node.op, ast.FloorDiv):
                if right == 0:
                    raise CalculationError("Cannot divide by zero")
                return float(left // right)
            raise CalculationError(f"Unsupported operator: {type(node.op).__name__}")

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise CalculationError("Security Error: Complex function calls disallowed")

            func_name = node.func.id
            args = [self._eval_node(arg) for arg in node.args]

            # Function mapping
            single_arg_funcs = {
                "sin": self._sin,
                "cos": self._cos,
                "tan": self._tan,
                "asin": self._asin,
                "acos": self._acos,
                "atan": self._atan,
                "sqrt": self._sqrt,
                "cbrt": self._cbrt,
                "log": self._log10,
                "log10": self._log10,
                "ln": self._ln,
                "log2": self._log2,
                "exp": math.exp,
                "fact": self._factorial,
                "factorial": self._factorial,
                "abs": abs,
                "deg": math.degrees,
                "rad": math.radians,
            }

            if func_name in single_arg_funcs:
                if len(args) != 1:
                    raise CalculationError(f"{func_name}() takes exactly 1 argument ({len(args)} given)")
                return float(single_arg_funcs[func_name](args[0]))

            if func_name == "pow":
                if len(args) != 2:
                    raise CalculationError("pow() takes exactly 2 arguments (base, exponent)")
                return float(self._power(args[0], args[1]))

            if func_name == "round":
                if len(args) == 1:
                    return float(round(args[0]))
                if len(args) == 2:
                    return float(round(args[0], int(args[1])))
                raise CalculationError("round() takes 1 or 2 arguments")

            raise CalculationError(f"Disallowed or unknown function: '{func_name}'")

        # Any other AST node type is forbidden (Attribute, Subscript, Import, Lambda, etc.)
        raise CalculationError(f"Security: Expression contains unauthorized construct '{type(node).__name__}'")

    # ----------------- Execution & Formatting -----------------

    def evaluate(self, expression: str) -> Tuple[bool, Union[float, int, str]]:
        """
        Parse and evaluate expression safely.
        :param expression: mathematical expression string
        :return: (success: bool, result_or_error_message)
        """
        cleaned = self.preprocess_expression(expression)
        if not cleaned:
            return True, 0

        # Safety: restrict length
        if len(cleaned) > 1000:
            return False, "Error: Expression too long"

        try:
            # Parse AST
            tree = ast.parse(cleaned, mode="eval")
            res = self._eval_node(tree)

            # Snap very close to zero to clean float imprecision
            if abs(res) < 1e-13:
                res = 0.0

            # Store last valid result
            self.last_result = res
            return True, res

        except CalculationError as ce:
            return False, str(ce)
        except ZeroDivisionError:
            return False, "Cannot divide by zero"
        except OverflowError:
            return False, "Calculation Overflow"
        except SyntaxError:
            return False, "Syntax Error"
        except Exception as e:
            return False, f"Error: {type(e).__name__}"

    def format_result(self, value: Union[float, int, str]) -> str:
        """
        Format calculation result cleanly for display.
        Removes unnecessary trailing zeros (.0) while maintaining precision.
        Uses scientific notation for very large or tiny numbers.
        """
        if isinstance(value, str):
            return value

        if math.isnan(value):
            return "NaN"
        if math.isinf(value):
            return "Infinity" if value > 0 else "-Infinity"

        # Check if it is a whole integer
        if math.isclose(value, round(value), abs_tol=1e-11) and abs(value) < 1e15:
            return f"{int(round(value)):,}".replace(",", " ")

        abs_val = abs(value)
        # Format very large or very small numbers with scientific notation
        if abs_val >= 1e14 or (0 < abs_val < 1e-6):
            formatted = f"{value:.8e}"
            # Clean up mantissa trailing zeros: 1.50000000e+15 -> 1.5e+15
            parts = formatted.split("e")
            mantissa = parts[0].rstrip("0").rstrip(".")
            return f"{mantissa}e{parts[1]}"

        # Standard precision representation
        formatted = f"{value:.10f}".rstrip("0").rstrip(".")
        if not formatted:
            return "0"

        # Separate integer and decimal part for nice thousands spacing if needed
        if "." in formatted:
            int_part, dec_part = formatted.split(".", 1)
            try:
                spaced_int = f"{int(int_part):,}".replace(",", " ")
                return f"{spaced_int}.{dec_part}"
            except ValueError:
                return formatted

        try:
            return f"{int(formatted):,}".replace(",", " ")
        except ValueError:
            return formatted
