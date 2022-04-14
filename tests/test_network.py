import json
import pytest

from pywrparser.parsers import PywrJSONParser

VALID_NETWORK_FILE = "tests/data/valid_network.json"

@pytest.fixture
def valid_network():
    with open(VALID_NETWORK_FILE, 'r') as fp:
        json_src = fp.read()

    parser = PywrJSONParser(json_src)
    parser.parse()

    return parser


def test_network_is_valid(valid_network):
    assert valid_network.has_errors == False
