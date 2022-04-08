from .base import PywrType
from pywrparser.types.exceptions import PywrValidationError

class PywrNode(PywrType):
    def __init__(self, data):
        self.data = data
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
            name = self.data.get("name")
            assert name is not None
        except:
            raise PywrValidationError("Missing node name")

        try:
            self.data["name"] = self.data["name"]
            assert isinstance(self.name, str)
        except:
            raise PywrValidationError("Invalid node name")

        try:
            assert "type" in self.data
        except:
            raise PywrValidationError(f"Node <{self.name}> does not define type")
