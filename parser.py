from primitives import *
from more_itertools import peekable
from tokenizer import Tokenizer


class Parser:

    def parse(self, source):
        t = Tokenizer()
        return self._parse(peekable(t.tokenize(source)))

    def _parse(self, it):
        if it.peek()[0] == "nil":
            next(it)
            return Nil()
        elif it.peek()[0] == "(":
            next(it)
            contents = []
            while it.peek()[0] != ")":
                contents.append(self._parse(it))
            next(it)  # consume )
            return List(contents)
        elif it.peek()[0] == "'":
            next(it)
            return quoted(self._parse(it))
        elif it.peek()[0] == "symbol":
            return Symbol(next(it)[1])
        else:
            return Number(next(it)[1])


def quoted(element):
    return List([Symbol("quote"), element])
