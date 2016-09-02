from tokenizer import *
import unittest


class TokenizerTest(unittest.TestCase):

    def setUp(self):
        self.t = Tokenizer()

    def assertTokenizing(self, string, equals):
        self.assertEqual(self.t.tokenize(string), equals)

    def test_tokenize_empty(self):
        self.assertTokenizing("", equals=[])

    def test_tokenize_nil(self):
        self.assertTokenizing("nil", equals=[("nil",)])

    def test_tokenize_parens(self):
        self.assertTokenizing("()", equals=[("(",), (")",)])

    def test_tokenize_ignore_spaces(self):
        self.assertTokenizing("( )nil  (", equals=[("(",), (")",), ("nil",), ("(",)])

    def test_tokenize_numbers(self):
        self.assertTokenizing("1 123 -1", equals=[("number", 1), ("number", 123), ("number", -1)])

    def test_tokenize_symbols(self):
        self.assertTokenizing("a ab c", equals=[("symbol", "a"), ("symbol", "ab"), ("symbol", "c")])

    def test_tokenize_quotes(self):
        self.assertTokenizing("'a", equals=[("'",), ("symbol", "a")])

    def test_tokenize_minus_symbol(self):
        self.assertTokenizing("- 1", equals=[("symbol", "-"), ("number", 1)])
