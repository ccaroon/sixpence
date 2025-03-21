from models.base import Base
from models.taggable import Taggable

class Expense(Taggable, Base):
    TYPE_INCOME = 0
    TYPE_EXPENSE = 1

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


    def update(self, data):
        self.type = data.get("type", self.type)
        self.date = data.get("date", self.date)
        self.icon = data.get("icon", self.icon)
        self.category = data.get("category", self.category)
        self.amount = data.get("amount", self.amount)

        self.tags = data.get("tags", self.tags)
