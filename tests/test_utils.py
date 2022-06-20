import pytest
from pywrparser.utils import (
    canonical_name,
    parse_reference_key
)

@pytest.mark.parametrize(
    ("name_title", "input_text", "expected"), [
        ("SIMPLE_CANONICAL", "__node__:attr", ("node", "attr") ),
        ("COMPLEX_CANONICAL", "__node extended(v2)__:attr name", ("node extended(v2)", "attr name"))
    ]
)
def test_parse_valid_names(name_title, input_text, expected):
    """
    Are references in canonical format correctly parsed?
    """
    assert parse_reference_key(input_text) == (expected[0], expected[1])


@pytest.mark.parametrize(
    ("input_node", "input_attr", "expected"), [
        ("node", "attr", "__node__:attr")
    ]
)
def test_canonical_names(input_node, input_attr, expected):
    """
    Are references correctly generated in canonical format?
    """
    assert canonical_name(input_node, input_attr) == expected
