from models.base import Base
from models.taggable import Taggable

class Expense(Taggable, Base):
    TYPE_INCOME = 0
    TYPE_EXPENSE = 1

    ROLLOVER_CATEGORY = "Sixpence:Rollover"
    ROLLOVER_ICON = "currency_exchange"

    def __init__(self, id=None, **kwargs):
        # Income or Expense
        self.type = self.TYPE_EXPENSE
        self.__date = None
        self.icon = None
        self.category = None
        self.amount = 0.0

        super().__init__(id=id, **kwargs)


    @property
    def date(self):
        return self.__date


    @date.setter
    def date(self, new_date):
        self.__date = self._date_setter(new_date)


    def __str__(self):
        return f"{self.id} | {self.date} | {self.category} | {self.amount}"


    def _serialize(self):
        data =  {
            "type": self.TYPE_EXPENSE if self.amount < 0.0 else self.TYPE_INCOME,
            "date": self.date.int_timestamp if self.date else None,
            "icon":self.icon,
            "category": self.category,
            "amount": self.amount
        }

        # Tags
        data.update(super()._serialize())

        return data

    @classmethod
    def update_rollover(cls, month, **kwargs):
        """
        Compute the balance at the end of the month previous to the given `month`.
        Then insert an Expense with that amount as the Starting Balance for the
        given `month`.

        Args:
            month (arrow) - Month for which to compute starting balance

        KWArgs:
            force_update (bool) - If rollover entry already exists, force it to be updated.
        """
        force_update = kwargs.get("force_update", False)
        month_start = month.floor("month")
        month_end = month.ceil("month")

        prev_month = month.shift(months=-1)
        prev_start = prev_month.floor("month")
        prev_end = prev_month.ceil("month")

        # Check if Rollover entry already exists for given `month`
        existing_entry = None
        entries = Expense.find(
            op="and",
            category=cls.ROLLOVER_CATEGORY,
            date=f"btw:{month_start.int_timestamp}:{month_end.int_timestamp}"
        )
        if entries and len(entries) == 1:
            existing_entry = entries[0]

        if not existing_entry or force_update:
            # Load data for prev month
            entries = Expense.find(
                date=f"btw:{prev_start.int_timestamp}:{prev_end.int_timestamp}"
            )

            # Compute ending balance for Previous Month
            income = 0.0
            expense = 0.0
            for entry in entries:
                if entry.amount >= 0.0:
                    income += entry.amount
                else:
                    expense += entry.amount

            entry_to_save = None
            if existing_entry:
                entry_to_save = existing_entry
                entry_to_save.amount = round(income + expense, 2)
            else:
                entry_to_save = Expense(
                    date=month_start,
                    icon=cls.ROLLOVER_ICON,
                    category=cls.ROLLOVER_CATEGORY,
                    amount=round(income + expense, 2),
                    tags=['Sixpence', 'Balance Rollover']
                )

            entry_to_save.save()


    def update(self, data):
        self.type = data.get("type", self.type)
        self.date = data.get("date", self.date)
        self.icon = data.get("icon", self.icon)
        self.category = data.get("category", self.category)
        self.amount = data.get("amount", self.amount)

        self.tags = data.get("tags", self.tags)


    @classmethod
    def collate_by_category(self, expenses:list):
        """
        Given a list of Expense items collate them by their category.

        Args:
            expenses (list): List of Budget itens

        Return:
            dict: Mapping of Expense items by their category.
        """
        expense_map = {}
        for exp in expenses:
            if exp.category in expense_map:
                expense_map[exp.category].append(exp)
            else:
                expense_map[exp.category] = [exp]

        return expense_map
