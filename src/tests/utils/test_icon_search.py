
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
        # Test kw mappings
        icons1 = self.__icon_search.smart_search("gas")
        self.assertTrue(len(icons1)> 0)

        icons2 = self.__icon_search.smart_search("fuel")
        self.assertTrue(len(icons2)> 0)

        self.assertEqual(icons1, icons2)

        # Test phrase
        icons = self.__icon_search.smart_search("I need gas for my car")
        for icn in icons:
            self.assertTrue("gas" in icn or "car" in icn)

        # Pluralize
        icons = self.__icon_search.smart_search("payment")
        self.assertTrue("payment" in icons)
        self.assertTrue("payments" in icons)

        # Len == 2
        icons = self.__icon_search.smart_search("tv")
        self.assertTrue(len(icons)> 0)
        self.assertTrue("connected_tv" in icons)

        # ignored words
        icons = self.__icon_search.smart_search("a the but for my")
        self.assertTrue(len(icons) == 0)


    def test_by_category(self):
        # Normal Category
        icons = self.__icon_search.by_category("Auto:Fuel")
        self.assertTrue(len(icons)> 0)

        for icn in icons:
            self.assertTrue("car" in icn or "gas" in icn)
