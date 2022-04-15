import contextlib
import functools
import inspect
import json
import re

from collections.abc import MutableMapping
from typing import Tuple

from pywrparser.types.exceptions import (
    PywrTypeValidationError,
    PywrTypeValidationErrorBundle
)
from pywrparser.types.warnings import PywrTypeValidationWarning


@contextlib.contextmanager
def raiseorpush(component: str, do_raise: bool, dest: MutableMapping):
    error_set = ()
    if not do_raise:
        error_set = (PywrTypeValidationError, PywrTypeValidationErrorBundle)

    try:
        yield
    except error_set as e:
        if isinstance(e, PywrTypeValidationErrorBundle):
            for eorw in e.bundle:
                if isinstance(eorw, Warning):
                    dest.warnings[component].append(eorw)
                elif isinstance(eorw, Exception):
                    dest.errors[component].append(eorw)


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
        setattr(inst, self.instattr, value)
        self.validate(inst, value)


    def validate(self, inst, value):
        ifuncs = inspect.getmembers(inst, inspect.ismethod)
        irules = { n:f for n,f in ifuncs if n.startswith("rule") }
        iwarns = { n:f for n,f in ifuncs if n.startswith("warn") }

        rules_passed = []
        rules_failed = []
        warnings = []

        exc_warn_bundle = []

        for w,f in iwarns.items():
            try:
                f()
            except AssertionError as e:
                value_text = self.trim_value(value)
                exc_warn_bundle.append(PywrTypeValidationWarning(inst.__class__.__qualname__, w, e, value_text))

        for r,f in irules.items():
            try:
                rules_passed.append(f"[PASSED] {r} -> {f()}")
            except AssertionError as e:
                value_text = self.trim_value(value)
                exc_warn_bundle.append(PywrTypeValidationError(inst.__class__.__qualname__, r, e, value_text))

        if self.store_passed_rules:
            inst.rules_passed = rules_passed

        if len(exc_warn_bundle) > 0:
            pveb = PywrTypeValidationErrorBundle(f"{inst.__class__.__qualname__} rule failures", exc_warn_bundle)
            raise pveb


    def trim_value(self, value):
        value_text = json.dumps(value)
        remainder = len(value_text) - self.max_value_len
        if remainder > 0:
            s = "s" if remainder > 1 else ""
            value_text = value_text[:self.max_value_len] + f"...[+{remainder} char{s}]"

        return value_text



def match(typename, fuzzy=False):
    def type_wrapper(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not (hasattr(self, "type") and self.type):
                return
            if fuzzy:
                is_match = typename.lower() in self.type.lower()
            else:
                is_match = typename.lower() == self.type.lower()

            if is_match:
                return func(self, *args, **kwargs)

        return wrapper
    return type_wrapper
