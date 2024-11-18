import unittest

from .mod import add_three


class TestAddThree(unittest.TestCase):
    def test_add_three(self):
        self.assertEqual(add_three(3), 6)
