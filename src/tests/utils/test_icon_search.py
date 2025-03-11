
import unittest

from utils.icon_search import IconSearch

class UtilTest(unittest.TestCase):
    def setUp(self):
        self.__icon_search = IconSearch()


    def test_by_keyword(self):
        # multiple matches
        icons = self.__icon_search.by_keyword("gas")
        self.assertTrue(len(icons)> 0)

        for icn in icons:
            self.assertIn("gas", icn)

        # exact match
        icons = self.__icon_search.by_keyword("blender")
        self.assertTrue(len(icons), 1)
        self.assertTrue(icons[0] == "blender")


    def test_smart_search(self):
        for kw in ("loan", "loans"):
            icons = self.__icon_search.smart_search(kw)
            self.assertTrue(len(icons) > 0)
            for icn in icons:
                self.assertIn("account_balance", icn)

        for kw in ("acorntv", "hulu", "netflix", "britbox"):
            icons = self.__icon_search.smart_search(kw)
            self.assertTrue(len(icons) > 0)
            self.assertIn("connected_tv", icons)

        for kw in ("tax", "taxes"):
            icons = self.__icon_search.smart_search(kw)
            self.assertTrue(len(icons) > 0)
            self.assertIn("money_off", icons)

        # No Mapping
        icons = self.__icon_search.smart_search("groceries")
        self.assertTrue(len(icons) > 0)
        self.assertIn("local_grocery_store", icons)

        # Test phrase
        icons = self.__icon_search.smart_search("I need gas for my car")
        for icn in icons:
            self.assertTrue("gas" in icn or "car" in icn)


    def test_by_category(self):
        # Normal Category
        icons = self.__icon_search.by_category("Auto:Fuel")
        self.assertTrue(len(icons)> 0)

        for icn in icons:
            self.assertTrue("car" in icn or "gas" in icn)
