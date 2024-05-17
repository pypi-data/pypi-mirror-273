import unittest
import unittest.mock

from example import use


@unittest.mock.patch("builtins.print")
class UseTestCase(unittest.TestCase):
    @unittest.expectedFailure
    @unittest.mock.patch("example.definition.Hey")
    def test_hey1(self, hey, print):
        hey.return_value.yo.return_value = 2
        self.assertEqual(use.do_something(), 3)

    @unittest.mock.patch("example.use.Hey.yo")
    def test_hey2(self, yo, print):
        yo.return_value = 3
        self.assertEqual(use.do_something(), 4)

    @unittest.mock.patch("example.use.CONSTANT", new=2)
    def test_hey3(self, print):
        self.assertEqual(use.do_something(), 3)
