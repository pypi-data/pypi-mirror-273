import doctest
import sys
import unittest
import unittest.runner

import pillory


def doctest_pillory():
    """
    >>> doctest_pillory()
    ... # doctest: +ELLIPSIS +REPORT_UDIFF
    definition imported
    x..
    ----------------------------------------------------------------------
    Ran 3 tests in ...
    <BLANKLINE>
    OK (expected failures=1)
    .../test_use.py... PM101 ...
    .../test_use.py... PM102 ...
    .../test_use.py... PM103 ...
    """

    class StdoutTestRunner(unittest.runner.TextTestRunner):
        def __init__(self, *args, **kwargs):
            kwargs["stream"] = sys.stdout
            super().__init__(*args, **kwargs)

    try:
        unittest.main(
            "example.test_use", testRunner=StdoutTestRunner, argv=sys.argv[:1]
        )
    except SystemExit:
        pass
    # If pillory imports the module again to lint it, it will run the print statement
    # inside. We want to prove pillory doesn't import the code it lints.
    del sys.modules["example.definition"]
    pillory.main(["example"])


if __name__ == "__main__":
    fail_count, test_count = doctest.testmod()
    if fail_count > 0:
        raise SystemExit(1)
    if test_count == 0:
        raise SystemExit("no doctests found")
