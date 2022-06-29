import json
import pytest

from pywrparser.parsers import PywrJSONParser


def test_errors_present(invalid_network):
    """
    An invalid network has some errors
    """
    assert invalid_network.has_errors is True


def test_metadata(invalid_network):
    """
    The metadata component is validated correctly
    """
    errors = invalid_network.errors

    """ No title key present """
    assert len(errors["metadata"]) == 1


def test_timestepper(invalid_network):
    """
    The timestepper component is validated correctly
    """
    errors = invalid_network.errors

    """ No end key present """
    assert len(errors["timestepper"]) == 1


def test_nodes(invalid_network):
    """
    Node errors are correctly identified
    """
    errors = invalid_network.errors

    """
    Node without name
    Node without type
    """
    assert len(errors["nodes"]) == 2


def test_edges(invalid_network):
    """
    Edge errors are correctly identified
    """
    errors = invalid_network.errors

    """
    Edge without target
    Edge target is source
    """
    assert len(errors["edges"]) == 2


def test_parameters(invalid_network):
    """
    Parameter errors are correctly identified
    """
    errors = invalid_network.errors

    """
    Parameter without type
    """
    assert len(errors["parameters"]) == 1


def test_recorders(invalid_network):
    """
    Recorder errors are correctly identified
    """
    errors = invalid_network.errors

    """
    Recorder without type
    """
    assert len(errors["recorders"]) == 1


def test_scenarios(invalid_network):
    """
    Scenario errors are correctly identified
    """
    errors = invalid_network.errors

    """
    Scenario without name
    """
    assert len(errors["scenarios"]) == 1


def test_network(invalid_network):
    """
    Network-level errors are correctly identified
    """
    errors = invalid_network.errors

    """
    Duplicate node name
    Duplicate parameter name
    Duplicate recorder name
    """
    assert len(errors["network"]) == 3


def test_duplicate_edges(invalid_network):
    """
    Duplicate edges are identified.
    One duplicate edge is present, with cardinality two
    """
    assert invalid_network.has_duplicate_edges
    assert len(invalid_network.duplicate_edges) == 1
    key = next(iter(invalid_network.duplicate_edges))
    assert invalid_network.duplicate_edges[key] == 2
