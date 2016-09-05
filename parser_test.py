import unittest
from parser import Parser
from primitives import *


class ParserTest(unittest.TestCase):

    def setUp(self):
        self.p = Parser()

    def assertParsingMany(self, source, equals):
        self.assertEqual(self.p.parse(source), StatementList(equals))

    def assertParsing(self, source, equals):
        self.assertParsingMany(source, [equals])

    def test_00_can_parse_nil(self):
        self.assertParsing("nil", equals=Nil())

    def test_01_can_parse_number(self):
        self.assertParsing("4", equals=Number(4))
        self.assertParsing("-5", equals=Number(-5))

    def test_02_can_parse_symbol(self):
        self.assertParsing("bla", equals=Symbol("bla"))

    def test_03_can_parse_empty_list(self):
        self.assertParsing("()", equals=List([]))

    def test_04_can_parse_one_element_list(self):
        self.assertParsing("(1)", equals=List([Number(1)]))

    def test_05_can_parse_nested_list(self):
        self.assertParsing("(())", equals=List([List([])]))

    def test_06_can_parse_many_elements_list(self):
        self.assertParsing("(1 2)", equals=List([Number(1), Number(2)]))

    def test_07_can_parse_quoted_symbols(self):
        self.assertParsing("'a", equals=List([Symbol("quote"), Symbol("a")]))

    def test_08_can_parse_boolean_literals(self):
        self.assertParsing("true", equals=Boolean(True))
        self.assertParsing("false", equals=Boolean(False))

    def test_09_can_parse_multiple_statements(self):
        self.assertParsingMany("2\n1", equals=[Number(2), Number(1)])
