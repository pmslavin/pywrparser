from .base import PywrType
from .exceptions import PywrValidationError

class PywrTimestepper(PywrType):
    def __init__(self, data):
        self.data = data
        self.validate()

    def validate(self):
        try:
            assert "start" in self.data
        except:
            raise PywrValidationError("Timestepper does not define 'start' key")

        try:
            assert "end" in self.data
        except:
            raise PywrValidationError("Timestepper does not define 'end' key")
