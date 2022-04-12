class PywrParserWarning(Warning):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.message})"


class PywrNameWarning(PywrParserWarning):
    def __init__(self, message):
        super().__init__(message)
