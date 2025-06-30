import unittest

from models.budget import Budget
from models.budget_group import BudgetGroup

class BudgetGroupTest(unittest.TestCase):

    def test_constructor(self):
        group = BudgetGroup("Auto:Fuel")

        self.assertEqual(group.category, "Auto:Fuel")
        self.assertEqual(group.spent, 0.0)

        # No Items, so these are undetermined as of yet
        self.assertEqual(group.type, None)
        self.assertEqual(group.icon, None)
        self.assertEqual(group.amount, 0.0)


    def test_basics(self):
        items = [
            Budget(
                category="Auto:Fuel",
                icon="fuel-pump",
                amount=-75.00,
                frequency=1
            ),
            Budget(
                category="Auto:Fuel",
                icon="fuel-pump",
                amount=-30.00,
                frequency=1
            ),
            Budget(
                category="Auto:Fuel",
                icon="fuel-pump",
                amount=-50.00,
                frequency=6
            ),
        ]
        # single item
        item = items[0]
        item_spent = -34.87
        group = BudgetGroup(item.category)
        group.add(item)
        group.spend(item_spent)
        self.assertEqual(group.icon, item.icon)
        self.assertEqual(group.type, Budget.TYPE_EXPENSE)
        self.assertEqual(group.amount, item.amount)
        self.assertEqual(group.monthly_avg, item.monthly_avg)
        self.assertEqual(group.spent, item_spent)

        # multiple
        group = BudgetGroup(items[0].category)
        grp_amt = 0.0
        grp_avg = 0.0
        grp_spent = 14.56
        for item in items:
            group.add(item)
            grp_amt += item.amount
            grp_avg += item.monthly_avg

        group.spend(grp_spent)
        self.assertEqual(group.icon, item.icon)
        self.assertEqual(group.type, Budget.TYPE_EXPENSE)
        self.assertEqual(group.amount, grp_amt)
        self.assertEqual(group.monthly_avg, grp_avg)
        self.assertEqual(group.spent, grp_spent)
