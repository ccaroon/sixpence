import flet as ft

from models.budget import Budget as BudgetItem

import views.constants as const

class Budget(ft.Container):
    def __init__(self, page):
        super().__init__(expand=True)

        self.__page = page
        self.__layout()


    def __layout(self):
        list_view = ft.ListView()

        # TODO:
        # - exclude deleted entries ... build into Base class?
        budget_items = BudgetItem.fetch(sort_by="type,category")
        for idx, item in enumerate(budget_items):
            income_color = const.COLOR_INCOME if idx % 2 == 0 else const.COLOR_INCOME_ALT
            exp_color = const.COLOR_EXPENSE if idx % 2 == 0 else const.COLOR_EXPENSE_ALT
            bgcolor = income_color if item.type == BudgetItem.TYPE_INCOME else exp_color

            tile = ft.ListTile(
                leading=ft.Icon(item.icon, color="black"),
                title=ft.Row(
                    [
                        ft.Text(item.category, color="black", expand=4),
                        ft.Text(f"${item.amount:0.2f}", color="black", expand=4),
                        ft.Text(item.notes, color="black", expand=4),
                    ],
                ),
                bgcolor=bgcolor
            )

            list_view.controls.append(tile)

        self.content = list_view


    def handle_keyboard_event(self, event):
        # print(f"Budget: KBE -> {event}")
        pass
