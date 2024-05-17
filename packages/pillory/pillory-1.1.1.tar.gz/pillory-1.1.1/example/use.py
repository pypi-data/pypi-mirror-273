"""Just an example module for tests."""

from example.definition import CONSTANT, Hey


def do_something():
    """Just an example function for tests."""
    value = Hey().yo() + CONSTANT
    print(value)
    return value
