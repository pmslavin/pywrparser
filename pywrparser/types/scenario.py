from .base import PywrType
from .exceptions import PywrValidationError

class PywrScenario(PywrType):
    def __init__(self, data):
        self.data = data

    @property
    def name(self):
        return str(self.data["name"])

    def validate(self):
        try:
            assert isinstance(self.name, str)
        except:
            raise PywrValidationError("Scenario has invalid name.")
