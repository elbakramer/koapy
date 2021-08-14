import collections

from functools import wraps
from inspect import signature


def string_to_list(s, sep=";"):
    if s is None:
        return s
    if not isinstance(s, str) and isinstance(s, collections.abc.Iterable):
        return s
    return s.rstrip(sep).split(sep) if s else []


def list_to_string(l, sep=";"):
    if l is None:
        return l
    if isinstance(l, str):
        return l
    if not isinstance(l, collections.abc.Iterable):
        return l
    return sep.join(l) if l else ""


def convert_list_arguments(*indices):
    def decorator(f):
        sig = signature(f)
        names = tuple(sig.parameters.keys())

        @wraps(f)
        def wrapper(*args, **kwargs):
            ba = sig.bind(*args, **kwargs)
            ba.apply_defaults()
            for i in indices:
                if isinstance(i, int):
                    i = names[i]
                if isinstance(i, str):
                    ba.arguments[i] = list_to_string(ba.arguments[i])
            args = ba.args
            kwargs = ba.kwargs
            return f(*args, **kwargs)

        return wrapper

    return decorator
