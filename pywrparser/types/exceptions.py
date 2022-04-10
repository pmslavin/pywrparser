
class PywrValidationError(Exception):
    def __init__(self, message, source=None, component=None):
        self.message = message
        self.source = source if source else {}
        self.component = component if component else ""
        super().__init__(self)

    def __str__(self):
        return f"<{self.__class__.__qualname__}> {self.component} {self.message}"
