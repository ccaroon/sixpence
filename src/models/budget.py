from .base import Base
from .taggable import Taggable

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


    def frequency_desc(self):
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
