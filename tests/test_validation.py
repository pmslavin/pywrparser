import json
import pytest

from pywrparser.parsers import PywrJSONParser

INVALID_ELEMENTS_FILE = "tests/data/invalid_elements.json"

@pytest.fixture
def invalid_elements():
    with open(INVALID_ELEMENTS_FILE, 'r') as fp:
        json_src = fp.read()

    parser = PywrJSONParser(json_src)
    parser.parse()

    return parser


def test_errors_present(invalid_elements):
    assert invalid_elements.has_errors == True


def test_metadata(invalid_elements):
    errors =  invalid_elements.errors

    """ No title key present """
    assert len(errors["metadata"]) == 1


def test_timestepper(invalid_elements):
    errors =  invalid_elements.errors

    """ No end key present """
    assert len(errors["timestepper"]) == 1


def test_nodes(invalid_elements):
    errors =  invalid_elements.errors

    """
    Node without name
    Node without type
    Duplicate node name
    """
    assert len(errors["nodes"]) == 3


def test_edges(invalid_elements):
    errors =  invalid_elements.errors

    """
    Edge without target
    Edge target is source
    """
    assert len(errors["edges"]) == 2


def test_parameters(invalid_elements):
    errors =  invalid_elements.errors

    """
    Parameter without type
    """
    assert len(errors["parameters"]) == 1


def test_recorders(invalid_elements):
    errors =  invalid_elements.errors

    """
    Recorder without type
    """
    assert len(errors["recorders"]) == 1


def test_scenarios(invalid_elements):
    errors =  invalid_elements.errors

    """
    Scenario without name
    """
    assert len(errors["scenarios"]) == 1


def test_network(invalid_elements):
    errors =  invalid_elements.errors

    """
    Duplicate node name
    Duplicate parameter name
    Duplicate recorder name
    """

    assert len(errors["network"]) == 3

