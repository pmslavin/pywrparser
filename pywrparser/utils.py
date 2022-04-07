import contextlib

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


def canonical_name(node, attr):
    return f"__{node}__:{attr}"
