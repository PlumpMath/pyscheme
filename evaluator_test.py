from evaluator import Evaluator
from parser import Parser
import unittest


class EvaluatorTest(unittest.TestCase):

    def assertEvaluating(self, expr1, equals):
        p = Parser()
        ev = Evaluator()
        context = {}
        self.assertEquals(ev.evaluate(p.parse(expr1), context), p.parse(equals))

    def test_00_nil_evaluates_to_nil(self):
        self.assertEvaluating("nil", equals="nil")

    def test_01_number_evaluates_to_itself(self):
        self.assertEvaluating("4", equals="4")

    def test_02_quoted_symbol_evaluates_to_quotation(self):
        self.assertEvaluating("'(1 2)", equals="(1 2)")

    def test_03_primitive_function_plus_evaluates_the_sum(self):
        self.assertEvaluating("(+ 3)", equals="3")
        self.assertEvaluating("(+ 3 5)", equals="8")
        self.assertEvaluating("(+ 3 5 -1)", equals="7")

    def test_04_primitive_function_minus_evaluates_the_difference(self):
        self.assertEvaluating("(- 3 5)", equals="-2")

    def test_05_other_primitive_arithmetic_functions(self):
        self.assertEvaluating("(* 3 5)", equals="15")
        self.assertEvaluating("(/ 10 2)", equals="5")

    def test_06_primitive_arithmetic_equal(self):
        self.assertEvaluating("(= 3 3)", equals="true")
        self.assertEvaluating("(= 3 4)", equals="false")
        self.assertEvaluating("(=)", equals="true")
        self.assertEvaluating("(= 3)", equals="true")
        self.assertEvaluating("(= 3 3 3)", equals="true")

    def test_07_primitive_not_inverts_boolean_value(self):
        self.assertEvaluating("(not true)", equals="false")
        self.assertEvaluating("(not false)", equals="true")

    def test_08_if_reduces_to_correct_clause(self):
        self.assertEvaluating("(if true 1 2)", equals="1")
        self.assertEvaluating("(if false 1 2)", equals="2")

    def test_09_list_defines_a_list(self):
        self.assertEvaluating("(list 1 2 3)", equals="(1 2 3)")

    def test_10_let_defines_a_value_for_a_symbol(self):
        self.assertEvaluating("(let ((a 1)) a)", equals="1")
