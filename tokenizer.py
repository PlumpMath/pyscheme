
class Tokenizer:

    def tokenize(self, string):
        return self._tokenize(string)

    def _tokenize(self, string):
        if not string:
            return []
        if string[0] == " ":
            return self._tokenize(string[1:])
        if string[0] in "()":
            return [(string[0],)] + self._tokenize(string[1:])
        if string.startswith("nil"):
            return [("nil",)] + self._tokenize(string[3:])

        # number
        s = ""
        while string and string[0] in "-1234567890":
            s += string[0]
            string = string[1:]
        if s:
            return [("number", eval(s))] + self._tokenize(string)

        # symbol
        while string and string[0] != " ":
            s += string[0]
            string = string[1:]
        return [("symbol", s)] + self._tokenize(string)
