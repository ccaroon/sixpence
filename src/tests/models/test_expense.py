import unittest
import random

import arrow

from models.expense import Expense

class ExpenseTest(unittest.TestCase):
    def __populate_db(self, count, date):
        """
        Generate some Expense items.

        Params:
            count (int): Number of entries to generate
            date (arrow): Base date for entries.
        """
        Expense.purge()

        base_date = date.ceil("month")

        for i in range(count):
            amt_mod = random.choice((-1,1))
            entry = Expense(
                date=base_date.shift(days=random.randint(0,27) * -1),
                icon=f"icon-entry-{i}",
                category=f"Test:Entry{i}",
                amount=round(random.random() * 100.00 * amt_mod, 2)

            )
            entry.save()


    # date, icon, category, amount
    def test_constructor(self):
        fields = {
            "date": arrow.now(),
            "icon": "gas-station",
            "category": "Auto:Fuel",
            "amount": -60.00,
        }
        item = Expense(**fields)

        self.assertEqual(item.date, fields["date"])
        self.assertEqual(item.icon, fields["icon"])
        self.assertEqual(item.category, fields["category"])
        self.assertEqual(item.amount, fields["amount"])


    def test_update_rollover(self):
        count = 25
        now = arrow.now()
        self.__populate_db(count, now.shift(months=-1))

        entries = Expense.fetch()
        self.assertEqual(len(entries), count)
        inc_amt = 0.0
        exp_amt = 0.0
        for entry in entries:
            if entry.amount >= 0.0:
                inc_amt += entry.amount
            else:
                exp_amt += entry.amount

        expected_balance = round(inc_amt + exp_amt, 2)

        Expense.update_rollover(now)

        entries = Expense.fetch()
        self.assertEqual(len(entries), count + 1)

        entries = Expense.find(category=Expense.ROLLOVER_CATEGORY)
        self.assertIsNotNone(entries)
        self.assertEqual(len(entries), 1)
        self.assertEqual(expected_balance, entries[0].amount)





#
