from functools import reduce


class Primitive:

    def __eq__(self, other):
        raise NotImplementedError


class Nil(Primitive):

    def __eq__(self, other):
        return isinstance(other, Nil)

    def evaluate(self):
        return self

    def __repr__(self):
        return "nil"


class Number(Primitive):

    def __init__(self, number):
        self._value = number

    def value(self):
        return self._value

    def __eq__(self, other):
        return self._value == other.value()

    def evaluate(self):
        return self

    def __repr__(self):
        return str(self._value)

    def __add__(self, other):
        return Number(self._value + other.value())

    def __sub__(self, other):
        return Number(self._value - other.value())

    def __mul__(self, other):
        return Number(self._value * other.value())

    def __truediv__(self, other):
        return Number(self._value / other.value())

    def __eq__(self, other):
        return Boolean(self._value == other.value())


class Boolean(Primitive):

    def __init__(self, value):
        self._value = value

    def value(self):
        return self._value

    def __eq__(self, other):
        return self._value == other.value()

    def __and__(self, other):
        return self._value and other.value()

    def __or__(self, other):
        return self._value or other.value()

    def __repr__(self):
        return str(self._value).lower()

    def evaluate(self):
        return self


class Symbol(Primitive):

    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    def __eq__(self, other):
        return self._name == other.name()

    def __repr__(self):
        return self._name

    def get_function(self):
        return ARITHMETIC_SYMBOLS[self._name]


ARITHMETIC_SYMBOLS = {
    "+": (lambda x, y: x + y),
    "-": (lambda x, y: x - y),
    "*": (lambda x, y: x * y),
    "/": (lambda x, y: x / y)
}


class List(Primitive):

    def __init__(self, elements):
        self._contents = elements[:]

    def contents(self):
        return self._contents[:]

    def __eq__(self, other):
        return self._contents == other.contents()

    def evaluate(self):
        # quoted only
        operand = self._contents[0]
        operands = self._contents[1:]
        assert(isinstance(operand, Symbol))
        name = operand.name()
        if name == "quote":
            return operands[0]
        if name in ARITHMETIC_SYMBOLS:
            return reduce(operand.get_function(), operands)
        if name == "=":
            return Boolean(not operands or all((o == operands[0]).value() for o in operands))
        if name == "not":
            return Boolean(not operands[0].value())
        if name == "if":
            assert 2 <= len(operands) <= 3, "if must have one condition and one or two clauses"
            if operands[0].value():
                return operands[1]
            else:
                return operands[2]
        raise Exception("can't evaluate symbol '%s'" % name)

    def __repr__(self):
        return "(" + " ".join(map(str, self._contents)) + ")"
