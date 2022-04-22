import json
import pytest

from pywrparser.types.network import PywrNetwork

from .fixtures import (
    INVALID_ELEMENTS_FILE,
    VALID_NETWORK_FILE
)


def test_network_from_file_is_valid():
    network, errors, warnings = PywrNetwork.from_file(VALID_NETWORK_FILE)
    assert network is not None
    assert errors is None


def test_network_from_json_is_valid():
    with open(VALID_NETWORK_FILE, 'r') as fp:
        src = fp.read()
    network, errors, warnings = PywrNetwork.from_json(src)
    assert network is not None
    assert errors is None

