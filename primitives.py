
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


class Symbol(Primitive):

    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    def __eq__(self, other):
        return self._name == other.name()

    def __repr__(self):
        return self._name


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
        return operands[0]

    def __repr__(self):
        return "(" + " ".join(map(str, self._contents)) + ")"
