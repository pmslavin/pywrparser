from .base import PywrType
from pywrparser.types.exceptions import PywrTypeValidationError

class PywrEdge(PywrType):
    def __init__(self, data):
        self.data = [str(d) for d in data]

    def __len__(self):
        return len(self.data)

    @property
    def is_simple(self):
        return len(self) == 2


    """ Validation rules """

    def rule_target_required(self):
        assert len(self) > 1, "Edge has no target"

    def rule_source_and_target_distinct(self):
        if len(self) > 1:
            assert self.data[0] != self.data[1], "Edge source and target are the same"
