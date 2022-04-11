import contextlib
import re

from collections.abc import MutableSequence

from pywrparser.types.exceptions import PywrValidationError

@contextlib.contextmanager
def raiseorpush(component: str, do_raise: bool, dest: MutableSequence):
    error_set = ()
    if not do_raise:
        error_set = PywrValidationError

    try:
        yield
    except error_set as e:
        dest[component].append(e)


def canonical_name(nodename, attr):
    return f"__{nodename}__:{attr}"


def parse_reference_key(key, strtok=':'):
    name, attr = key.split(strtok)
    name_pattern = r"^__[a-zA-Z0-9_ \.\-\(\)]+__$"
    if not re.search(name_pattern, name):
        raise ValueError(f"Invalid reference {name}")

    return name.strip('_'), attr
