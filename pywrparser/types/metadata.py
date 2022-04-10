from .base import PywrType
from .exceptions import PywrValidationError

class PywrMetadata(PywrType):
    def __init__(self, data):
        self.data = data
        self.validate()

    @property
    def title(self):
        return self.data["title"]

    def validate(self):
        try:
            assert isinstance(self.title, str)
        except:
            raise PywrValidationError("Metadata does not define 'title' key", self.data)
