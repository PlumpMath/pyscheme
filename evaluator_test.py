from primitives import *
from evaluator import Evaluator
from parser import Parser
import unittest


class EvaluatorTest(unittest.TestCase):

    def assertEvaluating(self, expr1, equals):
        p = Parser()
        ev = Evaluator()
        self.assertEquals(ev.evaluate(p.parse(expr1)), ev.evaluate(p.parse(equals)))

    def test_00_nil_evaluates_to_nil(self):
        self.assertEvaluating("nil", equals="nil")

    def test_01_number_evaluates_to_itself(self):
        self.assertEvaluating("4", equals="4")

    def test_02_quoted_symbol_evaluates_to_quotation(self):
        self.assertEvaluating("'(a 1)", equals="(a 1)")

    def test_03_primitive_function_plus_evaluates_the_sum(self):
        self.assertEvaluating("(+ 3)", equals="3")
        self.assertEvaluating("(+ 3 5)", equals="8")
        self.assertEvaluating("(+ 3 5 -1)", equals="7")

    def test_04_primitive_function_minus_evaluates_the_difference(self):
        self.assertEvaluating("(- 3 5)", equals="-2")

    def test_05_other_primitive_arithmetic_functions(self):
        self.assertEvaluating("(* 3 5)", equals="15")
        self.assertEvaluating("(/ 10 2)", equals="5")


