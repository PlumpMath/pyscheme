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


class Symbol(Primitive):

    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    def __eq__(self, other):
        return self._name == other.name()

    def __repr__(self):
        return self._name

    def is_arithmetic(self):
        return self._name in ARITHMETIC_SYMBOLS

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
        if operand == Symbol("quote"):
            return operands[0]
        if operand.is_arithmetic():
            return reduce(operand.get_function(), operands)

    def __repr__(self):
        return "(" + " ".join(map(str, self._contents)) + ")"
