
class Primitive:

    def __eq__(self, other):
        raise NotImplementedError


class Nil(Primitive):

    def __eq__(self, other):
        return isinstance(other, Nil)


class Number(Primitive):

    def __init__(self, number):
        self._value = number

    def value(self):
        return self._value

    def __eq__(self, other):
        return self._value == other.value()


class Symbol(Primitive):

    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    def __eq__(self, other):
        return self._name == other.name()


class List(Primitive):

    def __init__(self, elements):
        self._contents = elements[:]

    def contents(self):
        return self._contents[:]

    def __eq__(self, other):
        return self._contents == other.contents()
