import io
import pytest
from pywrparser.display import (
    console,
    write_results,
    results_as_dict
)


DUMMY_FILENAME = "filename.json"

def test_console_available():
    assert console is not None


def test_console_basic(valid_network):
    """
    Does the console contain the expected output given basic input?
    """
    console.file = io.StringIO()
    errors = valid_network.errors
    warnings = valid_network.warnings

    write_results(DUMMY_FILENAME, errors, warnings)

    output = console.file.getvalue()
    """
      Console output has header in the format...
        "Parser results for 'somefile.json': 10 errors, 3 warnings"
    """
    assert f"Parser results for \'{DUMMY_FILENAME}\': " in output
    assert "error" in output
    assert "warning" in output


def test_results_as_dict(valid_network, valid_network_file):
    """
    Are returned results in the correct format with expected content?
    """
    errors = valid_network.errors
    warnings = valid_network.warnings

    output = results_as_dict(valid_network_file, errors, warnings)
    assert isinstance(output, dict)
    assert "parse_results" in output
    if errors:
        assert "errors" in output
    if warnings:
        assert "warnings" in output
