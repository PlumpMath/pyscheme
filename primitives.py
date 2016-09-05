from functools import reduce


class Primitive:

    def __eq__(self, other):
        return str(self) == str(other)

    def __repr__(self):
        raise NotImplementedError

    def evaluate(self, context):
        raise NotImplementedError


class Nil(Primitive):

    def evaluate(self, context):
        return self

    def __repr__(self):
        return "nil"


class Number(Primitive):

    def __init__(self, number):
        self._value = number

    def value(self):
        return self._value

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
        return Number(self._value // other.value())


class Boolean(Primitive):

    def __init__(self, value):
        self._value = value

    def value(self):
        return self._value

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

    def evaluate(self, context):
        first = self._contents[0]
        rest = self._contents[1:]

        operator = first.evaluate(context)
        if isinstance(operator, Symbol):
            name = operator.name()
            if name == "if":
                assert 2 <= len(rest) <= 3, "`if` must have 1 condition and 1 or 2 clauses"
                return evaluate_if(rest[0], rest[1:3], context)
            elif name == "quote":
                assert len(rest) == 1, "`quote` must have 1 parameter"
                return rest[0]
            elif name == "let":
                assert len(rest) == 2, "`let` must have 2 parameters"
                return evaluate_let(rest[0], rest[1], context)
            elif name == "lambda":
                assert len(rest) == 2, "`lambda` must have 2 parameters"
                return Lambda(parameter_list=rest[0], code=rest[1])
            elif name == "define":
                assert len(rest) == 3, "`define` must have 3 parameters"
                name = rest[0].name()
                fun = Lambda(parameter_list=rest[1], code=rest[2])
                context[name] = fun
                return fun
            parameters = list(map(lambda e: e.evaluate(context), rest))
            if name in builtin:
                return builtin[name](parameters)
            else:
                raise Exception("can't evaluate symbol '%s'" % name)
        elif isinstance(operator, Lambda):
            parameters = list(map(lambda e: e.evaluate(context), rest))
            return operator.apply(parameters, context)
        else:
            raise Exception("can't evaluate '%s'" % operator)

    def __repr__(self):
        return "(" + " ".join(map(str, self._contents)) + ")"


builtin = {
    "if": None,
    "quote": None,
    "let": None,
    "lambda": None,
    "define": None,
    "list": lambda parameters: List(parameters),
    "=": lambda parameters: Boolean(not parameters or all(p == parameters[0] for p in parameters)),
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


class Lambda(Primitive):

    def __init__(self, parameter_list, code):
        self.parameter_list = parameter_list
        self.code = code

    def apply(self, arguments, outer_context):
        z = outer_context.copy()
        z.update(bind_arguments(self.parameter_list, arguments))
        return self.code.evaluate(z)

    def evaluate(self, context):
        return self

    def __repr__(self):
        return "(lambda " + self.parameter_list + " " + self.code + ")"


def parse_definitions(definitions):
    # ((a b) (c d) ...)
    result = {}
    for key_value in map(List.contents, definitions.contents()):
        assert len(key_value) == 2
        result[key_value[0].name()] = key_value[1]
    return result


def bind_arguments(parameter_list, arguments):
    # (a b c d)
    assert len(parameter_list.contents()) == len(arguments)
    return dict(zip(map(Symbol.name, parameter_list.contents()), arguments))


class StatementList(Primitive):

    def __init__(self, statements):
        self.statements = statements

    def evaluate(self, outer_context):
        context = outer_context.copy()
        last_value = None
        for statement in self.statements:
            last_value = statement.evaluate(context)
        return last_value

    def __repr__(self):
        return "\n".join(map(str, self.statements))
