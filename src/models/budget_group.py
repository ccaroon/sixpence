class BudgetGroup:
    def __init__(self, category):
        self.__category = category
        self.__spent = 0.0
        self.__items = []


    @property
    def category(self):
        """ The Group's Category """
        return self.__category


    @property
    def count(self):
        """ The number of Budget items in the Group """
        return len(self.__items)


    @property
    def type(self):
        """ The Group's Type: Income or Expense"""
        item_type = None
        if self.__items:
            # ASSUMES that all the budget items are the same type
            item_type = self.__items[0].type

        return item_type


    @property
    def icon(self):
        """ A representative icon for the Group """
        icon = None
        if self.__items:
            # Just use the first item's icon as a representation for the group
            icon = self.__items[0].icon

        return icon


    @property
    def amount(self):
        """ Amount Budgeted for the Category across all items in the Group """
        total = 0.0
        for item in self.__items:
            total += item.amount

        return total

    @property
    def amount_yearly(self):
        """
        Amount Budgeted for the Category across all items in the Group
        for the Year
        """
        total = 0.0
        for item in self.__items:
            total += item.amount * (12 / item.frequency)

        return total


    @property
    def spent(self):
        """ Amount spent towards the Group's total budgeted amount """
        return self.__spent


    @property
    def monthly_avg(self):
        """ The monthly average of all items in the Group """
        avg = 0.0
        for item in self.__items:
            avg += item.monthly_avg

        return avg


    def predict_spending(self, month):
        """
        Calculate the amount the should have been spent on the Group by the
        given `month`
        """
        amount = 0.0
        for item in self.__items:
            amount += item.predict_spending(month)

        return amount


    def spend(self, amount):
        """ Update the amount spent towards the Group """
        self.__spent += amount


    def add(self, item, spent=0.0):
        """ Add a Budgeted Item to the Group """
        self.__items.append(item)
        self.__spent += spent
