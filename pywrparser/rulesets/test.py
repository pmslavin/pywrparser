from pywrparser.types.node import PywrNode
from pywrparser.types.parameter import PywrParameter
from pywrparser.utils import match

__name__ = "Test Ruleset"
__version__ = "0.1.0"
__description__ = "A test ruleset for development purposes"


class AltNode(PywrNode):
    def __init__(self, data):
        super().__init__(data)

    def rule_no_xstart(self):
        if self.name:
            assert not self.name.lower().startswith('x'), "Node name may not begin with letter 'x'"


class AltParameter(PywrParameter):
    def __init__(self, name, data):
        super().__init__(name, data)

    def rule_no_ystart(self):
        assert not self.name.lower().startswith('y'), "Parameter name may not begin with letter 'y'"
