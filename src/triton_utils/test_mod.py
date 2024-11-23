import unittest

from .global_var import set_device
from .test import create_input


class TestAddThree(unittest.TestCase):
    def setUp(self):
        set_device("cpu")

    def test_add_three(self):
        s1, s2 = create_input((3, 3)).shape
        self.assertEqual(s1, 3)
        self.assertEqual(s2, 3)
