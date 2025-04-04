import flet as ft

import pprint

from models.expense import Expense

import utils.constants as const
from utils.locale import Locale
import utils.tools

class ExpenseNavBar(ft.AppBar):
    def __init__(self, page, parent, callbacks):
        self.__page = page
        self.__parent = parent

        self.__refresh = callbacks.get("on_refresh")
        self.__on_new = callbacks.get("on_new")
        self.__on_change_month = callbacks.get("on_change_month")

        self.__menu = ft.PopupMenuButton(
            icon=ft.Icons.MENU,
            items=[
                ft.PopupMenuItem(icon=ft.Icons.CURRENCY_EXCHANGE,
                    text="Recalculate Rollover", checked=False,
                    on_click=self.__on_recalc_rollover)
            ]
        )

        self.__date_picker = ft.ElevatedButton(
            self.__parent.current_date.format("MMM YYYY"),
            on_click=lambda e: self.__page.open(
                ft.DatePicker(
                    current_date=self.__parent.current_date,
                    on_change=self.__on_change_month
                )
            )
        )

        self.__search_control = ft.TextField(
            label="Search",
            prefix_icon=ft.Icons.SEARCH,
            on_submit=self.__on_search_submit)

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

        self.__view_control = ft.SegmentedButton(
            on_change=self.__on_view_change,
            selected={"progress"},
            segments=[
                ft.Segment(icon=ft.Icon(ft.Icons.BAR_CHART, color=ft.Colors.ON_PRIMARY_CONTAINER), value="progress"),
                ft.Segment(icon=ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.ON_PRIMARY_CONTAINER), value="calendar"),
                ft.Segment(icon=ft.Icon(ft.Icons.FORMAT_LIST_BULLETED, color=ft.Colors.ON_PRIMARY_CONTAINER), value="itemized")
            ]
        )

        super().__init__(
            leading=self.__menu,
            title=ft.Text("Expenses"),
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
                ft.IconButton(
                    data={"offset": 0},
                    icon=ft.Icons.CALENDAR_MONTH,
                    icon_color=ft.Colors.ON_PRIMARY_CONTAINER,
                    on_click=self.__on_change_month
                ),
                ft.IconButton(
                    data={"offset": -1},
                    icon=ft.Icons.ARROW_LEFT, on_click=self.__on_change_month),
                self.__date_picker,
                ft.IconButton(
                    data={"offset": 1},
                    icon=ft.Icons.ARROW_RIGHT, on_click=self.__on_change_month),
                ft.VerticalDivider(
                    color=ft.Colors.ON_PRIMARY_CONTAINER,
                    leading_indent=5, trailing_indent=5),
                self.__income_total,
                self.__expense_total,
                self.__net_balance,
                ft.VerticalDivider(
                    color=ft.Colors.ON_PRIMARY_CONTAINER,
                    leading_indent=5, trailing_indent=5),
                self.__view_control,
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

    @property
    def income_total(self):
        pass


    @property
    def expense_total(self):
        pass


    @property
    def net_balance(self):
        pass


    @income_total.setter
    def income_total(self, value):
        self.__income_total.label.value = Locale.currency(value)


    @expense_total.setter
    def expense_total(self, value):
        self.__expense_total.label.value = Locale.currency(value)


    @net_balance.setter
    def net_balance(self, value):
        self.__net_balance.label.value = Locale.currency(value)
        self.__net_balance.bgcolor = const.COLOR_INCOME if value >= 0.0 else const.COLOR_EXPENSE


    def change_view(self, view_name):
        """ ONLY updates the checkmark on the view control """
        # Setting selected does not seem to trigger on_change() :(
        self.__view_control.selected = {view_name}
        self.__view_control.update()


    def __on_recalc_rollover(self, evt):
        Expense.update_rollover(self.__parent.current_date, force_update=True)
        self.__refresh()


    def __on_view_change(self, evt):
        new_view = list(evt.control.selected)[0]
        self.__search_control.value = None
        self.__refresh(reset_filters=True, view=new_view)


    def __on_search_clear(self, evt):
        self.__search_control.value = None
        self.__refresh(reset_filters=True)


    def __on_search_submit(self, evt):
        value = evt.data

        # Looks like numeric/dollar amount i.e. a float sans '$'
        # Use the given value as a minium, i.e. search for all
        # budget items of that amount and more
        filters = {}
        if utils.tools.is_numeric(value):
            op = "gte" if float(value) >= 0 else "lte"
            filters["amount"] = f"{op}:{value}"
        else:
            # tags:my stuff
            if value.startswith("tags:"):
                (_, tag_name) = value.split(":",2)
                filters["tags"] = tag_name
            # Search in the category for the given string
            else:
                filters["category"] = value

        self.__refresh(
            reset_filters=True,
            **filters
        )
        self.__search_control.focus()


    def set_date_display(self, value):
        self.__date_picker.text = value


    def handle_keyboard_event(self, event):
        if event.ctrl or event.meta:
            if event.key == "F":
                self.__search_control.focus()
