from .base import PywrType

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
        assert len(self) > 1
