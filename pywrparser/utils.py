import contextlib
import inspect
import json
import re

from collections.abc import MutableMapping
from typing import Tuple

from pywrparser.types.exceptions import PywrTypeValidationError


@contextlib.contextmanager
def raiseorpush(component: str, do_raise: bool, dest: MutableMapping):
    error_set = ()
    if not do_raise:
        error_set = (PywrTypeValidationError,)

    try:
        yield
    except error_set as e:
        if hasattr(e, "rules_failed"):
            for rule in e.rules_failed:
                dest[component].append(rule)
        else:
            dest[component].append(e)


def canonical_name(nodename: str, attr: str) -> str:
    return f"__{nodename}__:{attr}"


def parse_reference_key(key: str) -> Tuple[str, str]:
    end_mark = "__:"
    name_end = key.rindex(end_mark) # ValueError on fail
    sepidx = name_end + len(end_mark) - 1
    name, attr = key[:sepidx], key[sepidx+1:]

    name_pattern = r"^__[a-zA-Z0-9_ \.\-\(\)]+__$"
    if not re.search(name_pattern, name):
        raise ValueError(f"Invalid reference: {name}")

    return name.strip('_'), attr


class PywrTypeValidator():

    def __init__(self, max_value_len=200, store_passed_rules=False):
        self.max_value_len = int(max_value_len)
        self.store_passed_rules = store_passed_rules


    def __set_name__(self, inst, name):
        self.instattr = '_' + name


    def __get__(self, inst, dtype=None):
        return getattr(inst, self.instattr)


    def __set__(self, inst, value):
        inst._data = value
        self.validate(inst, value)


    def validate(self, inst, value):
        ifuncs = inspect.getmembers(inst, inspect.ismethod)
        irules = { n:f for n,f in ifuncs if n.startswith("rule") }

        rules_passed = []
        rules_failed = []

        for r,f in irules.items():
            try:
                rules_passed.append(f"[PASSED] {r} -> {f()}")
            except AssertionError as e:
                value_text = json.dumps(value)
                remainder = len(value_text) - self.max_value_len
                if remainder > 0:
                    s = "s" if remainder > 1 else ""
                    value_text = value_text[:self.max_value_len] + f"...[+{remainder} char{s}]"
                rules_failed.append(f"[FAILED] {inst.__class__.__qualname__} '{r}' failed -> {e}:\n         {value_text}")

        if len(rules_failed) > 0:
            pve = PywrTypeValidationError(f"{inst.__class__.__qualname__} rule failures", source=value_text)
            pve.rules_failed = rules_failed
            raise pve
        elif self.store_passed_rules:
            inst.rules_passed = rules_passed
