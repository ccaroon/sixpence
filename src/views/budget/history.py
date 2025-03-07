import flet as ft

import arrow
import locale

from models.budget import Budget
import views.constants as const
import utils.tools as tools

class HistoryDialog(ft.AlertDialog):
    def __init__(self, page):
        super().__init__(modal=True)

        self.__item = None
        self.__page = page
        self.__layout()


    def __on_close(self, evt):
        self.open = False
        self.update()


    def __layout(self):
        self.__title_fld = ft.Text(
            "",
            weight=ft.FontWeight.BOLD,
            theme_style=ft.TextThemeStyle.DISPLAY_SMALL
        )
        self.__history_list = ft.ListView()

        self.title = self.__title_fld
        self.content = ft.Column(
                [
                    self.__history_list,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=self.__page.window.width // 2,
                height=self.__page.window.height // 2,
                scroll=ft.ScrollMode.AUTO
            )
        self.actions = [
            ft.ElevatedButton(
                "Close",
                color=ft.Colors.PRIMARY,
                on_click=self.__on_close
            )
        ]


    def __update_history(self):
        self.__history_list.controls.clear()

        for idx, hst in enumerate(self.__item.history):
            bgcolor = tools.cycle([
                ft.Colors.GREY_200, ft.Colors.GREY_400
            ], idx)
            date = arrow.get(hst["date"])

            amount = float(hst["amount"])
            next_amt = float(self.__item.amount)
            if idx < len(self.__item.history) - 1:
                next_hst = self.__item.history[idx + 1]
                next_amt = float(next_hst["amount"])

            # Increase
            # -- UP arrow
            # -- Bad / Red color / based on entry type
            icon = ft.Icons.KEYBOARD_DOUBLE_ARROW_UP
            icon_color = const.COLOR_EXPENSE if self.__item.type == Budget.TYPE_EXPENSE else const.COLOR_INCOME
            if abs(next_amt) < abs(amount):
                # Decrease
                # -- DN arrow
                # -- Good / Green color / based on entry type
                icon = ft.Icons.KEYBOARD_DOUBLE_ARROW_DOWN
                icon_color = const.COLOR_INCOME if self.__item.type == Budget.TYPE_EXPENSE else const.COLOR_EXPENSE

            tile = ft.ListTile(
                leading=ft.Icon(icon, color=icon_color),
                title=ft.Row(
                    [
                        ft.Text(date.format("MMM DD, YYYY"),
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=2),
                        ft.Text(
                            locale.currency(amount, grouping=True),
                            color="black",
                            # weight=ft.FontWeight.BOLD,
                            expand=1),
                        ft.Text(hst.get("note", "?????"),
                            color="black",
                            expand=3),
                        ft.Text(
                            locale.currency(next_amt, grouping=True),
                            color="black",
                            # weight=ft.FontWeight.BOLD,
                            expand=1),
                    ],
                ),
                bgcolor=bgcolor
            )

            self.__history_list.controls.append(tile)

        self.__history_list.update()


    def display(self, budget_item):
        self.__item = budget_item

        self.__title_fld.value = f"{self.__item.category} | {locale.currency(self.__item.amount)}/{self.__item.frequency_desc()}"
        self.__update_history()

        self.__page.open(self)
