from primitives import *
from evaluator import Evaluator
from parser import quoted
import unittest


class EvaluatorTest(unittest.TestCase):

    def test_00_nil_evaluates_to_nil(self):
        ev = Evaluator()
        self.assertEquals(ev.evaluate(Nil()), Nil())

    def test_01_number_evaluates_to_itself(self):
        ev = Evaluator()
        self.assertEquals(ev.evaluate(Number(4)), Number(4))

    def test_02_quoted_symbol_evaluates_to_quotation(self):
        ev = Evaluator()
        expr = List([Symbol("a"), Number(1)])
        self.assertEqual(ev.evaluate(quoted(expr)), expr)

    def test_03_primitive_function_plus_evaluates_the_sum(self):
        ev = Evaluator()
        expr = List([Symbol("+"), Number(3)])
        self.assertEqual(ev.evaluate(expr), Number(3))

        expr = List([Symbol("+"), Number(3), Number(5)])
        self.assertEqual(ev.evaluate(expr), Number(8))

        expr = List([Symbol("+"), Number(3), Number(5), Number(-1)])
        self.assertEqual(ev.evaluate(expr), Number(7))

    def test_04_primitive_function_minus_evaluates_the_difference(self):
        ev = Evaluator()
        expr = List([Symbol("-"), Number(3), Number(5)])
        self.assertEqual(ev.evaluate(expr), Number(-2))

    def test_05_other_primitive_arithmetic_functions(self):
        ev = Evaluator()
        expr = List([Symbol("*"), Number(3), Number(5)])
        self.assertEqual(ev.evaluate(expr), Number(15))

        expr = List([Symbol("/"), Number(10), Number(2)])
        self.assertEqual(ev.evaluate(expr), Number(5))

