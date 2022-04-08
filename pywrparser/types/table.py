from .base import PywrType
from pywrparser.types.exceptions import PywrValidationError

class PywrTable(PywrType):
    def __init__(self, name, data):
        self.data = data
        self.name = str(name)
        self.validate()

    @property
    def type(self):
        return self.data["type"]

    @property
    def attrs(self):
        return tuple(self.data.keys())

    def validate(self):
        try:
            assert isinstance(self.name, str)
        except:
            raise PywrValidationError("Invalid table name.")

        try:
            assert "url" in self.data
        except:
            raise PywrValidationError(f"Table <{self.name}> does not include url.")
