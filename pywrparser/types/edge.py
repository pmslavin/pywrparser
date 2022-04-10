from .base import PywrType
from pywrparser.types.exceptions import PywrValidationError

class PywrEdge(PywrType):
    def __init__(self, data):
        self.data = data
        self.validate()

    def __len__(self):
        return len(self.data)

    @property
    def is_simple(self):
        return len(self) == 2

    def validate(self):
        try:
            assert len(self) > 1
        except:
            raise PywrValidationError("Edge has no target", source=self.data)

        try:
            assert self.data[0] != self.data[1]
        except:
            raise PywrValidationError("Edge source and target are the same", source=self.data)
