import flet as ft

import locale

import utils.tools
import views.constants as const

from models.budget import Budget as BudgetItem
from views.base import Base as BaseView

class Budget(BaseView):

    def __init__(self, page):
        self.__filters = {"deleted_at": "null"}
        super().__init__(page)


    def _update(self):
        self.__list_view.controls.clear()

        # print(f"Filters: [{self.__filters}]")

        budget_items = BudgetItem.find(
            op="and",
            sort_by="type,category",
            **self.__filters
        )
        inc_total = 0.0
        exp_total = 0.0
        for idx, item in enumerate(budget_items):
            inc_color = utils.tools.cycle(
                (const.COLOR_INCOME, const.COLOR_INCOME_ALT), idx)
            exp_color = utils.tools.cycle(
                (const.COLOR_EXPENSE, const.COLOR_EXPENSE_ALT), idx)

            bgcolor = None
            if item.type == BudgetItem.TYPE_INCOME:
                bgcolor = inc_color
                inc_total += item.amount
            else:
                bgcolor = exp_color
                exp_total += item.amount

            # bgcolor = inc_color if item.type == BudgetItem.TYPE_INCOME else exp_color

            tile = ft.ListTile(
                leading=ft.Icon(item.icon, color="black"),
                title=ft.Row(
                    [
                        ft.Text(item.category, color="black", expand=4),
                        ft.Text(
                            locale.currency(item.amount),
                            color="black", expand=4),
                        # ft.Text(f"{item.frequency} months", color="black", expand=4),
                        ft.Text(item.notes, color="black", expand=4),
                        ft.VerticalDivider(),
                        ft.IconButton(ft.Icons.EDIT),
                        ft.IconButton(ft.Icons.DELETE)
                    ],
                ),
                subtitle=ft.Text(item.frequency_desc(), color="black"),
                bgcolor=bgcolor
            )

            self.__list_view.controls.append(tile)

        self.__income_total.text = locale.currency(inc_total, grouping=True)
        self.__expense_total.text = locale.currency(exp_total, grouping=True)

        self._page.update()


    def _layout(self):
        self.__list_view = ft.ListView()
        self.content = self.__list_view
        self._update()


    def __on_frequency_change(self, evt):
        new_freq = list(evt.control.selected)[0]

        if new_freq == "all":
            del self.__filters["frequency"]
        else:
            self.__filters["frequency"] = new_freq

        self._update()


    def __clear_search_filters(self):
        for field in ("amount", "category"):
            if field in self.__filters:
                del self.__filters[field]


    def __on_search_clear(self, evt):
        self.__clear_search_filters()
        self.__search_control.value = None
        self._update()


    def __on_search(self, evt):
        self.__clear_search_filters()

        value = evt.data

        # Looks like numeric/dollar amount i.e. a float sans '$'
        # Use the given value as a minium, i.e. search for all
        # budget items of that amount and more
        if utils.tools.is_numeric(value):
            op = "gte" if float(value) >= 0 else "lte"
            self.__filters["amount"] = f"{op}:{value}"
        # Search in the category for the given string
        else:
            if value:
                self.__filters["category"] = value

        self._update()
        self.__search_control.focus()


    def __on_new_item(self, evt):
        pass


    def _layout_navbar(self):
        self.__search_control = ft.TextField(
            label="Search", icon=ft.Icons.SEARCH, on_submit=self.__on_search)

        self.__income_total = ft.OutlinedButton(
            icon=ft.Icons.ATTACH_MONEY,
            style=ft.ButtonStyle(bgcolor=const.COLOR_INCOME)
        )
        self.__expense_total = ft.OutlinedButton(
            icon=ft.Icons.MONEY_OFF,
            style=ft.ButtonStyle(bgcolor=const.COLOR_EXPENSE)
        )

        self._navbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.FORMAT_LIST_BULLETED, size=const.ICON_MEDIUM),
            title=ft.Text("Budget"),
            bgcolor=ft.Colors.PRIMARY_CONTAINER,
            actions=[
                # New Budget Item Button
                ft.IconButton(
                    icon=ft.Icons.FORMAT_LIST_BULLETED_ADD,
                    on_click=self.__on_new_item),
                ft.VerticalDivider(),
                self.__income_total,
                self.__expense_total,
                ft.VerticalDivider(),
                # Frequency Filter buttons
                ft.SegmentedButton(
                    on_change=self.__on_frequency_change,
                    selected={"all"},
                    segments=[
                        ft.Segment(icon=ft.Icon(ft.Icons.FILTER_1), value=1),
                        ft.Segment(icon=ft.Icon(ft.Icons.FILTER_2), value=2),
                        ft.Segment(icon=ft.Icon(ft.Icons.FILTER_3), value=3),
                        ft.Segment(icon=ft.Icon(ft.Icons.FILTER_6), value=6),
                        ft.Segment(icon=ft.Icon(ft.Icons.CALENDAR_MONTH), value=12),
                        ft.Segment(icon=ft.Icon(ft.Icons.ALL_INCLUSIVE), value="all"),
                    ]
                ),
                ft.VerticalDivider(),
                # Search - Box and Reset button
                self.__search_control,
                ft.IconButton(
                    icon=ft.Icons.CLEAR,
                    on_click=self.__on_search_clear)
            ]
        )


    def handle_keyboard_event(self, event):
        if event.ctrl or event.meta:
            if event.key == "F":
                self.__search_control.focus()






#
