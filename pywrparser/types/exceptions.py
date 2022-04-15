class PywrParserException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.message})"


class PywrTypeValidationError(PywrParserException):
    def __init__(self, component, rule, exc, valuetext):
        self.component = component
        self.rule = rule
        self.exc = exc
        self.valuetext = valuetext

    def __str__(self):
        return f"[FAILURE] {self.component} '{self.rule}' -> {self.exc}:\n          {self.valuetext}"


class PywrTypeValidationErrorBundle(PywrParserException):
    def __init__(self, message, bundle):
        self.message = message
        self.bundle = bundle


class PywrNetworkValidationError(PywrParserException):
    def __init__(self, message):
        super().__init__(message)
