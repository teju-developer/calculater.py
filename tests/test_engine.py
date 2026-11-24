"""
Comprehensive Unit Tests for CalculatorEngine.
Verifies arithmetic, scientific functions, degree/radian conversions,
safe AST evaluation, and security attack prevention.
"""

import math
import sys
import os
import unittest

# Ensure calculator module is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from calculator.engine import CalculatorEngine, CalculationError


class TestCalculatorEngine(unittest.TestCase):

    def setUp(self):
        self.engine = CalculatorEngine(angle_mode="DEG")

    # 1. Basic Arithmetic
    def test_addition_and_subtraction(self):
        ok, res = self.engine.evaluate("15 + 27")
        self.assertTrue(ok)
        self.assertEqual(res, 42)

        ok, res = self.engine.evaluate("100 - 45.5")
        self.assertTrue(ok)
        self.assertEqual(res, 54.5)

        ok, res = self.engine.evaluate("-12 + 5")
        self.assertTrue(ok)
        self.assertEqual(res, -7)

    def test_multiplication_and_division(self):
        ok, res = self.engine.evaluate("6 * 7")
        self.assertTrue(ok)
        self.assertEqual(res, 42)

        ok, res = self.engine.evaluate("8 × 9")
        self.assertTrue(ok)
        self.assertEqual(res, 72)

        ok, res = self.engine.evaluate("144 / 12")
        self.assertTrue(ok)
        self.assertEqual(res, 12)

        ok, res = self.engine.evaluate("100 ÷ 4")
        self.assertTrue(ok)
        self.assertEqual(res, 25)

    def test_decimal_operations(self):
        ok, res = self.engine.evaluate("0.1 + 0.2")
        self.assertTrue(ok)
        self.assertAlmostEqual(res, 0.3, places=9)

        ok, res = self.engine.evaluate("3.14159 * 2")
        self.assertTrue(ok)
        self.assertAlmostEqual(res, 6.28318, places=4)

    def test_parentheses_and_order_of_operations(self):
        ok, res = self.engine.evaluate("2 + 3 * 4")
        self.assertTrue(ok)
        self.assertEqual(res, 14)

        ok, res = self.engine.evaluate("(2 + 3) * 4")
        self.assertTrue(ok)
        self.assertEqual(res, 20)

        ok, res = self.engine.evaluate("((10 - 2) * (3 + 1)) / 4")
        self.assertTrue(ok)
        self.assertEqual(res, 8)

        # Implicit multiplication
        ok, res = self.engine.evaluate("2(3 + 4)")
        self.assertTrue(ok)
        self.assertEqual(res, 14)

        ok, res = self.engine.evaluate("(2 + 1)(3 + 2)")
        self.assertTrue(ok)
        self.assertEqual(res, 15)

    def test_percentage_and_modulus(self):
        ok, res = self.engine.evaluate("50%")
        self.assertTrue(ok)
        self.assertEqual(res, 0.5)

        ok, res = self.engine.evaluate("200 * 15%")
        self.assertTrue(ok)
        self.assertEqual(res, 30)

        ok, res = self.engine.evaluate("17 % 5")
        self.assertTrue(ok)
        self.assertEqual(res, 2)

    # 2. Scientific Functions
    def test_square_root_and_powers(self):
        ok, res = self.engine.evaluate("sqrt(64)")
        self.assertTrue(ok)
        self.assertEqual(res, 8)

        ok, res = self.engine.evaluate("cbrt(27)")
        self.assertTrue(ok)
        self.assertEqual(res, 3)

        ok, res = self.engine.evaluate("2^3")
        self.assertTrue(ok)
        self.assertEqual(res, 8)

        ok, res = self.engine.evaluate("2**4")
        self.assertTrue(ok)
        self.assertEqual(res, 16)

    def test_trigonometric_degree_mode(self):
        self.engine.set_angle_mode("DEG")

        ok, res = self.engine.evaluate("sin(30)")
        self.assertTrue(ok)
        self.assertAlmostEqual(res, 0.5, places=6)

        ok, res = self.engine.evaluate("cos(60)")
        self.assertTrue(ok)
        self.assertAlmostEqual(res, 0.5, places=6)

        ok, res = self.engine.evaluate("cos(90)")
        self.assertTrue(ok)
        self.assertEqual(res, 0.0)

        ok, res = self.engine.evaluate("tan(45)")
        self.assertTrue(ok)
        self.assertAlmostEqual(res, 1.0, places=6)

        ok, res = self.engine.evaluate("asin(0.5)")
        self.assertTrue(ok)
        self.assertAlmostEqual(res, 30.0, places=5)

        ok, res = self.engine.evaluate("acos(0.5)")
        self.assertTrue(ok)
        self.assertAlmostEqual(res, 60.0, places=5)

        ok, res = self.engine.evaluate("atan(1)")
        self.assertTrue(ok)
        self.assertAlmostEqual(res, 45.0, places=5)

    def test_trigonometric_radian_mode(self):
        self.engine.set_angle_mode("RAD")

        ok, res = self.engine.evaluate("sin(pi / 6)")
        self.assertTrue(ok)
        self.assertAlmostEqual(res, 0.5, places=6)

        ok, res = self.engine.evaluate("cos(pi / 3)")
        self.assertTrue(ok)
        self.assertAlmostEqual(res, 0.5, places=6)

        ok, res = self.engine.evaluate("tan(pi / 4)")
        self.assertTrue(ok)
        self.assertAlmostEqual(res, 1.0, places=6)

    def test_logarithms(self):
        ok, res = self.engine.evaluate("log(100)")
        self.assertTrue(ok)
        self.assertEqual(res, 2.0)

        ok, res = self.engine.evaluate("log(1000)")
        self.assertTrue(ok)
        self.assertEqual(res, 3.0)

        ok, res = self.engine.evaluate("ln(e)")
        self.assertTrue(ok)
        self.assertAlmostEqual(res, 1.0, places=6)

        ok, res = self.engine.evaluate("log2(8)")
        self.assertTrue(ok)
        self.assertEqual(res, 3.0)

    def test_factorial(self):
        ok, res = self.engine.evaluate("5!")
        self.assertTrue(ok)
        self.assertEqual(res, 120)

        ok, res = self.engine.evaluate("fact(0)")
        self.assertTrue(ok)
        self.assertEqual(res, 1)

        ok, res = self.engine.evaluate("fact(6)")
        self.assertTrue(ok)
        self.assertEqual(res, 720)

    def test_constants_and_abs(self):
        ok, res = self.engine.evaluate("pi")
        self.assertTrue(ok)
        self.assertAlmostEqual(res, math.pi, places=9)

        ok, res = self.engine.evaluate("e")
        self.assertTrue(ok)
        self.assertAlmostEqual(res, math.e, places=9)

        ok, res = self.engine.evaluate("abs(-99.9)")
        self.assertTrue(ok)
        self.assertEqual(res, 99.9)

    # 3. Memory Operations
    def test_memory_functions(self):
        self.engine.memory_clear()
        self.assertFalse(self.engine.has_memory())

        self.engine.memory_store(50)
        self.assertTrue(self.engine.has_memory())
        self.assertEqual(self.engine.memory_recall(), 50)

        self.engine.memory_add(25)
        self.assertEqual(self.engine.memory_recall(), 75)

        self.engine.memory_subtract(15)
        self.assertEqual(self.engine.memory_recall(), 60)

        self.engine.memory_clear()
        self.assertEqual(self.engine.memory_recall(), 0)
        self.assertFalse(self.engine.has_memory())

    # 4. Error Handling and Domain Checks
    def test_division_by_zero(self):
        ok, msg = self.engine.evaluate("10 / 0")
        self.assertFalse(ok)
        self.assertIn("divide by zero", msg.lower())

        ok, msg = self.engine.evaluate("5 % 0")
        self.assertFalse(ok)
        self.assertIn("zero", msg.lower())

    def test_domain_errors(self):
        ok, msg = self.engine.evaluate("sqrt(-25)")
        self.assertFalse(ok)
        self.assertIn("Domain Error", msg)

        ok, msg = self.engine.evaluate("log(-10)")
        self.assertFalse(ok)
        self.assertIn("Domain Error", msg)

        ok, msg = self.engine.evaluate("ln(0)")
        self.assertFalse(ok)
        self.assertIn("Domain Error", msg)

        ok, msg = self.engine.evaluate("asin(2)")
        self.assertFalse(ok)
        self.assertIn("Domain Error", msg)

        ok, msg = self.engine.evaluate("fact(-5)")
        self.assertFalse(ok)
        self.assertIn("Factorial Error", msg)

    def test_invalid_syntax(self):
        ok, msg = self.engine.evaluate("2 ++ 3")  # in python ++ is unary +, so 2 + (+3) = 5
        self.assertTrue(ok)

        ok, msg = self.engine.evaluate("2 +* 3")
        self.assertFalse(ok)

        ok, msg = self.engine.evaluate("((2 + 3)")
        self.assertFalse(ok)

    # 5. Security - Unsafe Expression Rejection
    def test_security_rejections(self):
        attacks = [
            "__import__('os').system('dir')",
            "eval('2 + 2')",
            "exec('x = 1')",
            "open('README.md')",
            "getattr(__builtins__, 'help')",
            "[x for x in (1, 2, 3)]",
            "lambda x: x + 1",
            "import os",
            "globals()",
            "locals()",
            "(1).__class__",
            "sys.exit()",
            "exit()",
            "quit()",
        ]

        for attack in attacks:
            ok, msg = self.engine.evaluate(attack)
            self.assertFalse(ok, f"Security vulnerability! Attack was allowed: {attack}")


if __name__ == "__main__":
    unittest.main()
