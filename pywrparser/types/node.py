from .base import PywrType
from pywrparser.types.exceptions import PywrValidationError

class PywrNode(PywrType):
    def __init__(self, data):
        self.data = data
        self.data["name"] = str(self.data["name"])
        self.validate()

    @property
    def type(self):
        return self.data["type"]

    @property
    def name(self):
        return self.data["name"]

    @property
    def attrs(self):
        return tuple(self.data.keys())

    def validate(self):
        try:
            assert isinstance(self.name, str)
        except:
            raise PywrValidationError("Invalid node name.")

        try:
            assert "type" in self.data
        except:
            raise PywrValidationError(f"Node <{self.name}> does not define type.")
