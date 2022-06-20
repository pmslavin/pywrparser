import pytest

from pywrparser.utils import match
from pywrparser.types import PywrNode
from pywrparser.types.exceptions import PywrTypeValidationErrorBundle
from pywrparser.types.warnings import PywrTypeValidationWarning


NODE1_DATA = {
    "name": "Test Node 1",
    "type": "node_type_1",
    "value": 46
}

NODE2_DATA = {
    "name": "Test Node 2",
    "type": "node_type_2",
    "value": 23
}

class PywrTestNode(PywrNode):
    def __init__self(data):
        super().__init__(data)

    def warn_value_ceiling(self):
        assert self.data["value"] < 30, f"Value exceeds maximum"

    @match("node_type_2")
    def warn_value_floor(self):
        assert self.data["value"] > 50, f"Value beneath minimum"


def test_node_warning():
    """
    Custom Node class global warnings are correctly applied
    """
    try:
        node = PywrTestNode(NODE1_DATA)
    except PywrTypeValidationErrorBundle as b:
        assert len(b.warnings) == 1


def test_node_match_warning():
    """
    Custom Node class type-specific warnings are correctly applied
    """
    try:
        node = PywrTestNode(NODE2_DATA)
    except PywrTypeValidationErrorBundle as b:
        assert len(b.warnings) == 1
