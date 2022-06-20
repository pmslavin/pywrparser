import pytest

from pywrparser.parsers import PywrJSONParser


@pytest.fixture
def valid_network_file():
    return "data/valid_network.json"


@pytest.fixture
def invalid_network_file():
    return "data/invalid_network.json"


@pytest.fixture
def valid_network(valid_network_file):
    with open(valid_network_file, 'r') as fp:
        json_src = fp.read()

    parser = PywrJSONParser(json_src)
    parser.parse()

    return parser


@pytest.fixture
def invalid_network(invalid_network_file):
    with open(invalid_network_file, 'r') as fp:
        json_src = fp.read()

    parser = PywrJSONParser(json_src)
    parser.parse()

    return parser
