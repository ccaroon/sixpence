
import unittest

import utils.tools
class UtilTest(unittest.TestCase):

    def test_cycle(self):
        items = ["zero", "one", "two"]
        count = len(items)

        for idx in range(0, 42):
            value = utils.tools.cycle(items, idx)
            self.assertIsNotNone(value)
            self.assertIn(value, items)
            self.assertEqual(value, items[idx % count])


    def test_is_numeric(self):
        self.assertTrue(utils.tools.is_numeric("123"))
        self.assertTrue(utils.tools.is_numeric("-123"))
        self.assertTrue(utils.tools.is_numeric("123.34"))
        self.assertTrue(utils.tools.is_numeric("-453.22"))
        self.assertTrue(utils.tools.is_numeric("-123.123"))
        self.assertTrue(utils.tools.is_numeric("+1.2"))
        self.assertTrue(utils.tools.is_numeric("+11.23"))
        self.assertFalse(utils.tools.is_numeric("+foobar-43"))
        self.assertFalse(utils.tools.is_numeric("foobar"))
        self.assertFalse(utils.tools.is_numeric("-42foobar"))
        self.assertFalse(utils.tools.is_numeric(""))
