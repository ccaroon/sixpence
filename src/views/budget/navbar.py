import flet as ft

import re

import utils.constants as const
from utils.locale import Locale
import utils.tools

class BudgetNavBar(ft.AppBar):
    def __init__(self, page, callbacks):
        self.__page = page

        self.__refresh = callbacks.get("on_refresh")
        self.__on_new = callbacks.get("on_new")

        self.__menu = ft.PopupMenuButton(
            icon=ft.Icons.MENU,
            items=[
                ft.PopupMenuItem(icon=ft.Icons.FORMAT_LIST_BULLETED,
                    text="Active Items", checked=True,
                    on_click=self.__on_active_items),
                ft.PopupMenuItem(icon=ft.Icons.ARCHIVE,
                    text="Archived Items", checked=False,
                    on_click=self.__on_archived_items),
                ft.PopupMenuItem(icon=ft.Icons.CALENDAR_MONTH,
                    text="By Month", checked=False,
                    on_click=self.__on_month_view)
            ]
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

        super().__init__(
            leading=self.__menu,
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


    def __on_active_items(self, evt):
        for choice in self.__menu.items:
            choice.checked = False

        evt.control.checked = True
        self.__refresh(deleted_at="null")


    def __on_archived_items(self, evt):
        for choice in self.__menu.items:
            choice.checked = False

        evt.control.checked = True
        self.__refresh(deleted_at="gt:0")


    def __on_month_view(self, evt):
        banner = ft.Banner(
            leading=ft.Icon(
                ft.Icons.WARNING,
                color=ft.Colors.YELLOW, size=const.ICON_MEDIUM),
            content=ft.Text("Month View is not yet implemented!",
                color=ft.Colors.ON_SECONDARY_CONTAINER),
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            actions=[
                ft.TextButton("Ok",
                    on_click=lambda evt: self.__page.close(banner))
            ]
        )
        self.__page.open(banner)


    def __on_frequency_change(self, evt):
        new_freq = list(evt.control.selected)[0]
        if new_freq == "all":
            new_freq = None

        self.__refresh(frequency=new_freq)


    def __on_search_clear(self, evt):
        self.__search_control.value = None
        self.__refresh(reset_filters=True)


    def __on_search_submit(self, evt):
        value = evt.data

        filters = {}

        # <field_name>=<query_string>
        # Ex: category=Pets | amount=gte:100 | type=0
        matches = re.match(r"(\w+)=", value)
        if matches:
            field = matches.group(1)
            (_, query) = value.split("=", 2)

            # TODO: handle tag aliases for "tags" searches

            # date=2025-03-30:2025-04-12
            if field == "date":
                (start, end) = query.split(":", 2)
                start_date = Locale.as_arrow(start).floor("day")
                end_date = Locale.as_arrow(end).ceil("day")
                query = f"btw:{start_date.int_timestamp}:{end_date.int_timestamp}"

            filters[field] = query
        # Looks like numeric/dollar amount i.e. a float sans '$'
        # Use the given value as a minium, i.e. search for all
        # budget items of that amount and more
        elif utils.tools.is_numeric(value):
            op = "gte" if float(value) >= 0 else "lte"
            filters["amount"] = f"{op}:{value}"
        # Default to searching in `category`
        else:
            filters["category"] = value

        self.__refresh(
            reset_filters=True,
            **filters
        )
        self.__search_control.focus()


    def handle_keyboard_event(self, event):
        if event.ctrl or event.meta:
            if event.key == "F":
                self.__search_control.focus()







#
