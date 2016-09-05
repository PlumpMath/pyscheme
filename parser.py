from primitives import *
from more_itertools import peekable
from tokenizer import Tokenizer


class Parser:

    def parse(self, source):
        t = Tokenizer()
        return self._parse_statements(peekable(t.tokenize(source)))

    def _parse_statements(self, it):
        statements = []
        while it.peek(None):
            statements.append(self._parse_statement(it))
        return StatementList(statements)

    def _parse_statement(self, it):
        if it.peek()[0] == "nil":
            next(it)
            return Nil()
        elif it.peek()[0] == "(":
            next(it)
            contents = []
            while it.peek()[0] != ")":
                contents.append(self._parse_statement(it))
            next(it)  # consume )
            return List(contents)
        elif it.peek()[0] == "'":
            next(it)
            return quoted(self._parse_statement(it))
        elif it.peek()[0] == "symbol":
            if it.peek()[1] in ("true", "false"):
                return Boolean(next(it)[1] == "true")
            else:
                return Symbol(next(it)[1])
        else:
            return Number(next(it)[1])


def quoted(element):
    return List([Symbol("quote"), element])
