from pywrparser.types.node import PywrNode
from pywrparser.types.parameter import PywrParameter
from pywrparser.utils import match

__key__ = "strict"
__ruleset_name__ = "Strict Ruleset"
__version__ = "0.1.0"
__description__ = "A strict ruleset for development purposes"


class StrictNode(PywrNode):
    def __init__(self, data):
        super().__init__(data)

    def rule_no_xstart(self):
        if self.name:
            assert not self.name.lower().startswith('x'), "StrictNode name may not begin with letter 'x'"


class StrictParameter(PywrParameter):
    def __init__(self, name, data):
        super().__init__(name, data)

    def rule_no_ystart(self):
        assert not self.name.lower().startswith('y'), "StrictParameter name may not begin with letter 'y'"
