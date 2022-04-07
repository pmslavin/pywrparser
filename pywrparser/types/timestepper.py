from .base import PywrType

class PywrTimestepper(PywrType):
    def __init__(self, data):
        self.data = data
        self.validate()

    def validate(self):
        assert "start" in self.data
        assert "end" in self.data
