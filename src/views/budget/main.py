import flet as ft

import locale
import pprint

import utils.tools
import views.constants as const

from models.budget import Budget as BudgetItem
from views.base import Base as BaseView
from views.budget.editor import BudgetEditor
from views.budget.history.view import HistoryView

class BudgetView(BaseView):

    def __init__(self, page):
        self.__filters = {"deleted_at": "null"}
        super().__init__(page)

        self.__editor = BudgetEditor(self._page, on_save=self._update)


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
                inc_total += (item.amount / item.frequency)
            else:
                bgcolor = exp_color
                exp_total += (item.amount / item.frequency)

            display_amt = f"{locale.currency(item.amount, grouping=True)}"
            if item.frequency > 1:
                display_amt += f" ({locale.currency(item.amount / item.frequency, grouping=True)})"

            has_history = len(item.history) > 0

            tile = ft.ListTile(
                leading=ft.Icon(item.icon, color="black"),
                title=ft.Row(
                    [
                        ft.Text(item.category,
                            color="black",
                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                            weight=ft.FontWeight.BOLD,
                            expand=4),
                        ft.Text(
                            display_amt,
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=4),
                        ft.Text(item.notes, color="black", expand=4),
                        ft.VerticalDivider(),
                        ft.IconButton(ft.Icons.HISTORY,
                            data=item,
                            icon_color=ft.Colors.GREY_800 if has_history else ft.Colors.GREY_500,
                            disabled=not has_history,
                            on_click=self.__on_history
                        ),
                        ft.IconButton(ft.Icons.EDIT,
                            data=item,
                            icon_color=ft.Colors.GREY_800,
                            on_click=self.__on_edit
                        ),
                        ft.IconButton(ft.Icons.DELETE,
                            data=item,
                            icon_color=ft.Colors.GREY_800,
                            on_click=self.__on_delete
                        )
                    ],
                ),
                subtitle=ft.Text(f"{item.frequency_desc()} / {const.MONTH_NAMES[item.first_due]}", color="black"),
                bgcolor=bgcolor
            )

            self.__list_view.controls.append(tile)

        self.__income_total.label.value = locale.currency(
            inc_total, grouping=True)
        self.__expense_total.label.value = locale.currency(
            exp_total, grouping=True)
        net_balance = inc_total + exp_total
        self.__net_balance.label.value = locale.currency(
            net_balance, grouping=True
        )
        self.__net_balance.bgcolor = const.COLOR_INCOME if net_balance >= 0 else const.COLOR_EXPENSE

        self._page.update()


    def _layout(self):
        self.__list_view = ft.ListView()
        self.content = self.__list_view

        self.__history_view = HistoryView(self._page)
        self._page.overlay.append(self.__history_view)

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


    def __on_edit(self, evt):
        budget_item = evt.control.data
        self.__editor.edit(budget_item)


    def __on_new(self, evt):
        budget_item = BudgetItem()
        self.__editor.edit(budget_item)


    def __on_history(self, evt):
        budget_item = evt.control.data
        self.__history_view.display(budget_item)


    def __on_delete(self, evt):
        # TODO: implement Archive capability
        # ...i.e. mark as deleted
        budget_item = evt.control.data
        budget_item.delete(safe=True)
        self._update()


    # TODO: factor out to a new class
    def _layout_navbar(self):
        self.__search_control = ft.TextField(
            label="Search",
            prefix_icon=ft.Icons.SEARCH,
            on_submit=self.__on_search)

        self.__income_total = ft.Chip(
            label=ft.Text("", color="black", size=18),
            leading=ft.Icon(ft.Icons.ATTACH_MONEY, color="black", size=20),
            bgcolor=const.COLOR_INCOME_ALT,
            # `on_click` is required or the Chip default to being disabled
            on_click=lambda evt: None
        )
        self.__expense_total =ft.Chip(
            label=ft.Text("", color="black", size=18),
            leading=ft.Icon(ft.Icons.MONEY_OFF, color="black", size=20),
            bgcolor=const.COLOR_EXPENSE_ALT,
            # `on_click` is required or the Chip default to being disabled
            on_click=lambda evt: None
        )
        self.__net_balance =ft.Chip(
            label=ft.Text("", color="black", size=18),
            leading=ft.Icon(ft.Icons.MONEY_ROUNDED, color="black", size=20),
            bgcolor=const.COLOR_INCOME,
            # `on_click` is required or the Chip default to being disabled
            on_click=lambda evt: None
        )

        self._navbar = ft.AppBar(
            leading=ft.Icon(
                ft.Icons.FORMAT_LIST_BULLETED,
                size=const.ICON_MEDIUM),
            title=ft.Text("Budget"),
            bgcolor=ft.Colors.PRIMARY_CONTAINER,
            actions=[
                # New Budget Item Button
                ft.IconButton(
                    icon=ft.Icons.FORMAT_LIST_BULLETED_ADD,
                    icon_color=ft.Colors.ON_PRIMARY_CONTAINER,
                    on_click=self.__on_new),
                ft.VerticalDivider(
                    color=ft.Colors.ON_PRIMARY_CONTAINER,
                    leading_indent=5, trailing_indent=5),
                self.__income_total,
                self.__expense_total,
                self.__net_balance,
                ft.VerticalDivider(
                    color=ft.Colors.ON_PRIMARY_CONTAINER,
                    leading_indent=5, trailing_indent=5),
                # Frequency Filter buttons
                ft.SegmentedButton(
                    on_change=self.__on_frequency_change,
                    selected={"all"},
                    segments=[
                        ft.Segment(icon=ft.Icon(ft.Icons.FILTER_1, color=ft.Colors.ON_PRIMARY_CONTAINER), value=1),
                        ft.Segment(icon=ft.Icon(ft.Icons.FILTER_2, color=ft.Colors.ON_PRIMARY_CONTAINER), value=2),
                        ft.Segment(icon=ft.Icon(ft.Icons.FILTER_3, color=ft.Colors.ON_PRIMARY_CONTAINER), value=3),
                        ft.Segment(icon=ft.Icon(ft.Icons.FILTER_6, color=ft.Colors.ON_PRIMARY_CONTAINER), value=6),
                        ft.Segment(icon=ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.ON_PRIMARY_CONTAINER), value=12),
                        ft.Segment(icon=ft.Icon(ft.Icons.ALL_INCLUSIVE, color=ft.Colors.ON_PRIMARY_CONTAINER), value="all"),
                    ]
                ),
                ft.VerticalDivider(
                    color=ft.Colors.ON_PRIMARY_CONTAINER,
                    leading_indent=5, trailing_indent=5),
                # Search - Box and Reset button
                self.__search_control,
                ft.IconButton(
                    icon=ft.Icons.CLEAR,
                    icon_color=ft.Colors.ON_PRIMARY_CONTAINER,
                    on_click=self.__on_search_clear)
            ]
        )


    def handle_keyboard_event(self, event):
        if event.ctrl or event.meta:
            if event.key == "F":
                self.__search_control.focus()
            elif event.key == "N":
                self.__on_new(None)
