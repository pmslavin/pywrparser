from .base import PywrType
from .exceptions import PywrValidationError

class PywrParameter(PywrType):
    def __init__(self, name, data):
        self.name = str(name)
        self.data = data
        self.validate()

    @property
    def type(self):
        return self.data["type"]

    @property
    def attrs(self):
        return tuple(self.data.keys())

    def validate(self):
        try:
            assert isinstance(self.type, str)
        except:
            raise PywrValidationError(f"Parameter <{self.name}> does not define type", self.data)
