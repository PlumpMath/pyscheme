from functools import reduce
# from more_itertools import peekable


class Primitive:

    def __eq__(self, other):
        raise NotImplementedError

    def evaluate(self, context):
        raise NotImplementedError


class Nil(Primitive):

    def __eq__(self, other):
        return isinstance(other, Nil)

    def evaluate(self, context):
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

    def evaluate(self, context):
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

    def evaluate(self, context):
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

    def evaluate(self, context):
        name = self._name
        if name in context:
            return context[name]
        elif name in builtin:
            return self
        else:
            raise Exception("Symbol '%s' not defined" % name)


class List(Primitive):

    def __init__(self, elements):
        self._contents = elements[:]

    def contents(self):
        return self._contents[:]

    def __eq__(self, other):
        return self._contents == other.contents()

    def evaluate(self, context):
        first = self._contents[0]
        rest = self._contents[1:]

        operator = first.evaluate(context)
        name = operator.name()
        assert isinstance(operator, Symbol)
        if name == "if":
            assert 2 <= len(rest) <= 3, "`if` must have one condition and one or two clauses"
            return evaluate_if(rest[0], rest[1:3], context)
        elif name == "quote":
            assert len(rest) == 1, "`quote` must have one parameter"
            return rest[0]
        elif name == "let":
            assert len(rest) == 2, "`let` must have two parameters"
            return evaluate_let(rest[0], rest[1], context)
        parameters = list(map(lambda e: e.evaluate(context), rest))
        if name in builtin:
            return builtin[name](parameters)
        else:
            raise Exception("can't evaluate symbol '%s'" % name)

    def __repr__(self):
        return "(" + " ".join(map(str, self._contents)) + ")"


builtin = {
    "if": None,
    "quote": None,
    "let": None,
    "list": lambda parameters: List(parameters),
    "=": lambda parameters: Boolean(not parameters or all((p == parameters[0]).value() for p in parameters)),
    "+": lambda parameters: reduce(Number.__add__, parameters),
    "-": lambda parameters: reduce(Number.__sub__, parameters),
    "*": lambda parameters: reduce(Number.__mul__, parameters),
    "/": lambda parameters: reduce(Number.__truediv__, parameters),
    "not": lambda parameters: Boolean(not parameters[0].value())
}


def evaluate_if(condition, clauses, context):
    selected_clause = clauses[0] if condition.value() else clauses[1]
    return selected_clause.evaluate(context)


def evaluate_let(definitions, code, outer_context):
    z = outer_context.copy()
    z.update(parse_definitions(definitions))
    return code.evaluate(z)


def parse_definitions(definitions):
    # ((a b) (c d) ...)
    result = {}
    for key_value in map(List.contents, definitions.contents()):
        assert len(key_value) == 2
        result[key_value[0].name()] = key_value[1]
    return result
