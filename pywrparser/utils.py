import contextlib
import re

from collections.abc import MutableMapping
from typing import Tuple

from pywrparser.types.exceptions import PywrValidationError


@contextlib.contextmanager
def raiseorpush(component: str, do_raise: bool, dest: MutableMapping):
    error_set = ()
    if not do_raise:
        error_set = (PywrValidationError,)

    try:
        yield
    except error_set as e:
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
