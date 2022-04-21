import pytest

from pywrparser.parsers import PywrJSONParser

VALID_NETWORK_FILE = "tests/data/valid_network.json"
INVALID_ELEMENTS_FILE = "tests/data/invalid_elements.json"


@pytest.fixture
def valid_network():
    with open(VALID_NETWORK_FILE, 'r') as fp:
        json_src = fp.read()

    parser = PywrJSONParser(json_src)
    parser.parse()

    return parser


@pytest.fixture
def invalid_elements():
    with open(INVALID_ELEMENTS_FILE, 'r') as fp:
        json_src = fp.read()

    parser = PywrJSONParser(json_src)
    parser.parse()

    return parser
