import unittest

from utils.locale import Locale

class UtilTest(unittest.TestCase):
    def setUp(self):
        Locale.init("en_US.UTF-8")


    def test_currency(self):
        amount = 17723.45654

        formatted_amt = Locale.currency(amount)
        self.assertEqual(formatted_amt, "$17,723.46")
