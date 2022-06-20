import pytest

from pywrparser import rules


def test_all_rulesets_complete():
    """
    Does each defined ruleset contain the required attributes?
    """
    rulesets = rules.get_rulesets()
    for ruleset_key, data in rulesets.items():
        ruleset_mod = rules.get_ruleset_module(ruleset_key)
        assert ruleset_key == ruleset_mod.__key__
        assert data["name"] == ruleset_mod.__ruleset_name__
        assert data["version"] == ruleset_mod.__version__
        assert data["description"] == ruleset_mod.__description__
