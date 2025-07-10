import re

from models.base import Base
from models.budget_group import BudgetGroup
from models.taggable import Taggable

class Budget(Taggable, Base):

    TYPE_INCOME = 0
    TYPE_EXPENSE = 1

    FREQ_DESC = {
        1: "Monthly",
        2: "Bi-Monthly",
        3: "Quarterly",
        6: "Bi-Yearly",
        12: "Yearly"
    }

    def __init__(self, id=None, **kwargs):
        # Income or Expense
        self.type = self.TYPE_EXPENSE
        self.icon = None
        self.category = None
        self.amount = 0.0
        # Month of the Year: 1 = Jan, 2 = Feb ... 12 = Dec
        self.first_due = 1
        # In Months
        self.frequency = 1
        # History -> {date, amount, note}
        self.history = []

        super().__init__(id=id, **kwargs)


    def __str__(self):
        return f"{self.id} | {self.category} | {self.amount}"


    def _serialize(self):
        data =  {
            "type": self.TYPE_EXPENSE if self.amount < 0.0 else self.TYPE_INCOME,
            "icon":self.icon,
            "category": self.category,
            "amount": self.amount,
            "first_due": self.first_due,
            "frequency": self.frequency
        }

        # Fix "date" in history
        history = self.history.copy()
        for entry in history:
            # Arrow -> INT epoch
            entry["date"] = entry["date"].int_timestamp
        data["history"] = history

        # Tags
        data.update(super()._serialize())

        return data


    @property
    def monthly_avg(self):
        """ The average amount spent on this Budget Item per Month """
        return round(self.amount / self.frequency, 2)


    def predict_spending(self, month):
        """
        Calculate the amount that should have been spent on this Budget item
        by the given `month`
        """
        amount = 0.0
        due_months = self.due_months()
        for due_mnth in due_months:
            if month >= due_mnth:
                amount += self.amount

        return round(amount, 2)


    def frequency_desc(self):
        """
        Items frequency as a descriptive strint

        Return:
            str: Description fo the frequency value

        Example:
            1 => Monthly
            3 => Quarterly
            12 => Yearly
            14 => 14 months
        """
        return self.FREQ_DESC.get(self.frequency, f"{self.frequency} months")


    def update(self, data):
        self.type = data.get("type", self.type)
        self.icon = data.get("icon", self.icon)
        self.category = data.get("category", self.category)
        self.amount = data.get("amount", self.amount)
        self.first_due = data.get("first_due", self.first_due)
        self.frequency = data.get("frequency", self.frequency)
        self.history = data.get("history", self.history)

        # history.date to Arrow
        for entry in self.history:
            entry["date"] = self._date_setter(entry["date"])

        self.tags = data.get("tags", self.tags)


    @classmethod
    def normalize_category(cls, value:str):
        """
        Normalize a category name

        Params:
            value(str): A Category name to be normalized

        Returns:
            str: Normalized category name

        Examples:
            Auto:Fuel -> Auto:Fuel
            auto:fuel -> Auto:Fuel
            personal:eating out -> Personal:Eating Out
        """
        parts = value.split(":")
        cat_parts = []
        for part in parts:
            if re.search(r"\s", part):
                sub_parts = part.split()
                sub_values = []
                for sub_part in sub_parts:
                    sub_part = sub_part.strip()
                    # Preserve case if is all uppercase string
                    # E.g. Personal:HABA != Personal:Haba
                    if sub_part.isupper():
                        sub_values.append(sub_part)
                    else:
                        sub_values.append(sub_part.capitalize())
                cat_parts.append(" ".join(sub_values))
            else:
                # Preserve case if is all uppercase string
                # E.g. Personal:HABA != Personal:Haba
                if part.isupper():
                    cat_parts.append(part)
                else:
                    cat_parts.append(part.capitalize())

        category = ":".join(cat_parts)
        return category


    @classmethod
    def categories(cls):
        """
        Category Name to Icon Name mapping

        Returns:
            dict: key -> category_name | value -> icon_name
        """
        items = cls.fetch(sort_by="category")
        categories = {}

        for item in items:
            categories[item.category] = item.icon

        return categories


    def due_months(self):
        """
        Compute a list of months that this item is due based on frequency and
        first_due month.

        Returns:
            list[int]: list of month numbers
        """
        due_months = []
        will_get = (12 - self.first_due) + 1
        more_needed = 12 - will_get

        for m in range(self.first_due, 12 + more_needed + 1, self.frequency):
            month = m if m <= 12 else m - 12
            due_months.append(month)

        return due_months


    # TODO: Get rid of this in favor of Budget.group()
    @classmethod
    def collate_by_category(self, budget:list):
        """
        Given a list of Budget items collate them by their category.

        Args:
            budget (list): List of Budget itens

        Return:
            dict: Mapping of Budget items by their category.
        """
        budget_map = {}
        for item in budget:
            if item.category not in budget_map:
                budget_map[item.category] = {
                    "type": item.type,
                    "icon": item.icon,
                    "category": item.category,
                    "amount": item.amount,
                    "spent": 0.0
                }
            else:
                budget_map[item.category]["amount"] += item.amount

        return budget_map


    @classmethod
    def group(self, budget:list):
        """
        Given a list of Budget items group them by their category.

        Args:
            budget (list): List of Budget itens

        Return:
            dict: Mapping of Budget items by their category to BudgetGroups.
        """
        budget_map = {}
        for item in budget:
            if item.category not in budget_map:
                budget_group = BudgetGroup(item.category)
                budget_group.add(item)
                budget_map[item.category] = budget_group
            else:
                budget_group = budget_map[item.category]
                budget_group.add(item)

        return budget_map


    @classmethod
    def for_month(cls, month_num:int, **kwargs):
        """
        All non-deleted budgeted items that are **due** in the given month

        Args:
            month_num (int): A month number: 1 to 12

        KWArgs:
            args to further filter the result set

        Returns:
            list[Budget]: List of Budget items.
        """
        items = cls.find(op="and", deleted_at="null", **kwargs)
        wanted_items = []
        for itm in items:
            if month_num in itm.due_months():
                wanted_items.append(itm)

        return wanted_items
