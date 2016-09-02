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
        print(ev.evaluate(quoted(expr)))
        self.assertEqual(ev.evaluate(quoted(expr)), expr)
