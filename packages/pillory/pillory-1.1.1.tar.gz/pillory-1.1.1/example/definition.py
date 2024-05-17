"""Just an example module for tests."""


class Hey:
    """Just an example class for tests."""

    def yo(self):
        """Just an example method for tests."""
        return 1


CONSTANT = 1

# This print is here to prove in the doctest that no code is imported during linting.
print("definition imported")
