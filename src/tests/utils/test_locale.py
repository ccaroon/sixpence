import unittest

from utils.locale import Locale

class UtilTest(unittest.TestCase):
    # def setUp(self):
    #     Locale.init()


    def test_currency(self):
        amount = 17723.45654

        # en_US
        Locale.init("en_US")
        formatted_amt = Locale.currency(amount)
        self.assertEqual(formatted_amt, "$17,723.46")

        Locale.init("en_UK")
        formatted_amt = Locale.currency(amount)
        self.assertEqual(formatted_amt, "£17,723.46")
