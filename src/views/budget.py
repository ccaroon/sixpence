import flet as ft

from models.budget import Budget as BudgetItem

class Budget(ft.Container):
    def __init__(self, page):
        super().__init__()

        # TODO: remove this / just a test
        b = BudgetItem(category="Groceries")
        b.save()

        self.__page = page
        self.__layout()


    def __layout(self):
        self.content = ft.Text(
            "Budget Placeholder",
            weight=ft.FontWeight.BOLD,
            theme_style=ft.TextThemeStyle.DISPLAY_LARGE)
