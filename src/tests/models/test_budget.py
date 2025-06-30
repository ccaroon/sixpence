import unittest
import random

from models.budget import Budget

class BudgetTest(unittest.TestCase):

    def __populate_db(self, dist):
        """
        Generate some Budget items

        Params:
            dist (list): List of tuples. Each tuple consist of three values
                         (count, frequency, first_due)
        """
        Budget.purge()

        for dst in dist:
            count = dst[0]
            freq = dst[1]
            fdue = dst[2]

            for i in range(count):
                item = Budget(
                    icon=f"icon-freq{freq}-fdue{fdue}-{i}",
                    category=f"Test:Freq{freq}Due{fdue}:Item{i}",
                    amount=random.random() * 100.00 * -1,
                    first_due=fdue,
                    frequency=freq
                )
                item.save()


    def test_constructor(self):
        fields = {
            "icon": "gas-station",
            "category": "Auto:Fuel",
            "amount": -60.00,
            "first_due": 1,
            "frequency": 1
        }
        item = Budget(**fields)

        self.assertEqual(item.icon, fields["icon"])
        self.assertEqual(item.category, fields["category"])
        self.assertEqual(item.amount, fields["amount"])
        self.assertEqual(item.first_due, fields["first_due"])
        self.assertEqual(item.frequency, fields["frequency"])


    def test_monthly_avg(self):
        test_data = {
            "monthly": {
                "fields": {
                    "icon": "gas-station",
                    "category": "Auto:Fuel",
                    "amount": -60.00,
                    "first_due": 1,
                    "frequency": 1
                },
                "expected": -60.00
            },
            "quarterly": {
                "fields": {
                    "icon": "bug",
                    "category": "Home:Pest Control",
                    "amount": -75.00,
                    "first_due": 1,
                    "frequency": 3
                },
                "expected": -25.00
            },
            "yearly": {
                "fields": {
                    "icon": "delivery-truck",
                    "category": "Subscriptions:Amazon Prime",
                    "amount": -149.00,
                    "first_due": 1,
                    "frequency": 12
                },
                "expected": -12.42
            }
        }

        for label, data in test_data.items():
            item = Budget(**data["fields"])
            self.assertEqual(item.monthly_avg, data["expected"])


    def test_due_months(self):
        fields = {
            "icon": "alien",
            "category": "Test:Due Months",
            "amount": -42.77
        }
        item = Budget(**fields)

        # monthly
        item.first_due = 1
        item.frequency = 1
        months = item.due_months()
        self.assertListEqual(months, [1,2,3,4,5,6,7,8,9,10,11,12])

        # bi-monthly
        # --> start jan
        item.first_due = 1
        item.frequency = 2
        months = item.due_months()
        self.assertListEqual(months, [1,3,5,7,9,11])

        # --> start feb
        item.first_due = 2
        item.frequency = 2
        months = item.due_months()
        self.assertListEqual(months, [2,4,6,8,10,12])

        # --> start march
        item.first_due = 3
        item.frequency = 2
        months = item.due_months()
        self.assertListEqual(months, [3,5,7,9,11,1])

        # quarterly
        # --> start jan
        item.first_due = 1
        item.frequency = 3
        months = item.due_months()
        self.assertListEqual(months, [1,4,7,10])

        # --> start feb
        item.first_due = 2
        item.frequency = 3
        months = item.due_months()
        self.assertListEqual(months, [2,5,8,11])

        # bi-yearly
        # --> start jan
        item.first_due = 1
        item.frequency = 6
        months = item.due_months()
        self.assertListEqual(months, [1,7])

        # --> start apr
        item.first_due = 4
        item.frequency = 6
        months = item.due_months()
        self.assertListEqual(months, [4,10])

        # yearly
        # --> start jan
        item.first_due = 1
        item.frequency = 12
        months = item.due_months()
        self.assertListEqual(months, [1])

        # --> start feb
        item.first_due = 2
        item.frequency = 12
        months = item.due_months()
        self.assertListEqual(months, [2])

        # --> start oct
        item.first_due = 10
        item.frequency = 12
        months = item.due_months()
        self.assertListEqual(months, [10])


    # Month x Freq Table (First Due = 1)
    #    -----------------------------------
    #    01 02 03 04 05 06 07 08 09 10 11 12
    # 1   x  x  x  x  x  x  x  x  x  x  x  x
    # 2   x     x     x     x     x     x
    # 3   x        x        x        x
    # 6   x                 x
    # 12  x
    #    ------------------------------------
    #     5  1  2  2  2  1  4  1  2  2  2  1
    def test_for_month(self):
        self.__populate_db([
            # count, freq, first_due
            (5, 1, 1),
            (5, 2, 1),
            (5, 3, 1),
            (5, 6, 1),
            (5, 12, 1)
        ])

        # month, expected count
        tests = [
            (1, 25),  (2, 5),   (3, 10),
            (4, 10),  (5, 10),  (6, 5),
            (7, 20),  (8, 5),   (9, 10),
            (10, 10), (11, 10), (12, 5),
        ]

        for test in tests:
            items = Budget.for_month(test[0])
            self.assertIsNotNone(items)
            self.assertEqual(len(items), test[1])







#
