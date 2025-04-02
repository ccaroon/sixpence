import flet as ft

import arrow
import pprint

import utils.tools
from utils.locale import Locale
import utils.constants as const

from models.budget import Budget
from models.expense import Expense
from views.base import Base as BaseView
from views.expenses.editor import ExpenseEditor

class ExpensesView(BaseView):

    def __init__(self, page):
        now = Locale.now()
        self.__start_date = now.floor("month")
        self.__end_date = now.ceil("month")

        Expense.update_rollover(now)

        self.__filters = {
            "date": f"btw:{self.__start_date.int_timestamp}:{self.__end_date.int_timestamp}"
        }
        super().__init__(page)

        self.__budget = Budget.for_month(self.__start_date.month)
        self.__editor = ExpenseEditor(self._page, on_save=self._update)


    def _update(self):
        self.__list_view.controls.clear()

        # pprint.pprint(f"Filters: [{self.__filters}]")
        expenses = Expense.find(
            op="and",
            sort_by="type,date",
            **self.__filters
        )
        inc_total = 0.0
        exp_total = 0.0

        for idx, item in enumerate(expenses):
            inc_color = utils.tools.cycle(const.INCOME_COLORS, idx)
            inc_color_alt = utils.tools.cycle(const.INCOME_COLORS, idx+1)
            exp_color = utils.tools.cycle(const.EXPENSE_COLORS, idx)
            exp_color_alt = utils.tools.cycle(const.EXPENSE_COLORS, idx+1)

            bgcolor = None
            tag_color = None
            if item.type == Expense.TYPE_INCOME:
                bgcolor = inc_color
                tag_color = inc_color_alt
                inc_total += item.amount
            else:
                bgcolor = exp_color
                tag_color = exp_color_alt
                exp_total += item.amount

            display_amt = f"{Locale.currency(item.amount)}"

            tags = []
            for tag_name in item.tag_list():
                tags.append(
                    ft.Chip(
                        label=ft.Text(tag_name),
                        bgcolor=tag_color,
                        on_click=self.__filter_by_tag,
                        padding=ft.padding.all(0)
                    )
                )

            tile = ft.ListTile(
                leading=ft.Icon(item.icon, color="black"),
                title=ft.Row(
                    [
                        ft.Text(item.category,
                            color="black",
                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                            weight=ft.FontWeight.BOLD,
                            expand=3),
                        ft.Text(
                            display_amt,
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=3),
                        ft.Row(tags, expand=4),
                        ft.VerticalDivider(),
                        # NOTE: if icon_color is set, then disabled_color has
                        #       no effect
                        #       Instead, have to adjust icon_color accoriding
                        #       to if the button is disabled
                        ft.IconButton(ft.Icons.EDIT,
                            data=item,
                            icon_color=ft.Colors.GREY_500 if item.deleted_at else ft.Colors.GREY_800,
                            on_click=self.__on_edit,
                            disabled=item.deleted_at is not None,
                        ),
                        ft.IconButton(ft.Icons.DELETE_FOREVER,
                            data=item,
                            icon_color=ft.Colors.GREY_500 if item.deleted_at else ft.Colors.GREY_800,
                            on_click=self.__on_delete_confirm,
                            disabled=item.deleted_at is not None
                        )
                    ],
                ),
                subtitle=ft.Text(
                    item.date.format("MMM DD, YYYY"),
                    color="black"),
                bgcolor=bgcolor
            )

            self.__list_view.controls.append(tile)

        self.__income_total.label.value = Locale.currency(inc_total)
        self.__expense_total.label.value = Locale.currency(exp_total)
        net_balance = inc_total + exp_total
        self.__net_balance.label.value = Locale.currency(net_balance)
        self.__net_balance.bgcolor = const.COLOR_INCOME if net_balance >= 0 else const.COLOR_EXPENSE

        self._page.update()


    def _layout(self):
        self.__list_view = ft.ListView()
        self.content = self.__list_view
        self.__layout_dlg()
        self._update()


    def __clear_search_filters(self):
        for field in ("amount", "category", "tags"):
            if field in self.__filters:
                del self.__filters[field]


    def __on_search_clear(self, evt):
        self.__clear_search_filters()
        self.__search_control.value = None
        self._update()


    def __filter_by_tag(self, evt):
        self.__filters["tags"] = evt.control.label.value
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
        else:
            # tags:my stuff
            if value.startswith("tags:"):
                (_, tag_name) = value.split(":",2)
                self.__filters["tags"] = tag_name
            # Search in the category for the given string
            else:
                self.__filters["category"] = value

        self._update()
        self.__search_control.focus()


    def __on_edit(self, evt):
        expense = evt.control.data
        self.__editor.edit(expense, self.__budget)


    def __on_new(self, evt):
        expense = Expense(
            date=Locale.now()
        )
        self.__editor.edit(expense, self.__budget)


    def __on_delete(self, evt):
        self._page.close(self.__confirm_dlg)

        if evt.control.text == "Yes":
            expense = self.__confirm_dlg.data
            expense.delete()
            self._update()


    def __on_delete_confirm(self, evt):
        item = evt.control.data

        self.__confirm_dlg.content = ft.Column(
            [
                ft.Text("Are you sure you want to delete this Expense?"),
                ft.Text(
                    f"{item.date.format("MMM DD, YYYY")} | {item.category} | {Locale.currency(item.amount)}?",
                    weight=ft.FontWeight.BOLD
                )
            ],
            tight=True
        )

        self.__confirm_dlg.data = item
        self._page.open(self.__confirm_dlg)


    def __set_month(self, date:arrow.arrow.Arrow):
        self.__start_date = date.floor("month")
        self.__end_date = date.ceil("month")

        self.__filters["date"] = f"btw:{self.__start_date.int_timestamp}:{self.__end_date.int_timestamp}"

        self.__date_picker.text = self.__start_date.format("MMM YYYY")

        self.__budget = Budget.for_month(self.__start_date.month)
        self._update()


    def __on_current_month(self, evt):
        self.__set_month(Locale.now())


    def __on_date_change(self, evt):
        chosen_date = arrow.get(evt.control.value)
        self.__set_month(chosen_date)


    def __on_prev_month(self, evt):
        prev_month = self.__start_date.shift(months=-1)
        self.__set_month(prev_month)


    def __on_next_month(self, evt):
        next_month = self.__start_date.shift(months=+1)
        self.__set_month(next_month)


    def __on_recalc_rollover(self, evt):
        Expense.update_rollover(self.__start_date, force_update=True)
        self._update()


    # TODO: factor out to a new class
    def _layout_navbar(self):
        self.__menu = ft.PopupMenuButton(
            icon=ft.Icons.MENU,
            items=[
                ft.PopupMenuItem(icon=ft.Icons.CURRENCY_EXCHANGE,
                    text="Recalculate Rollover", checked=False,
                    on_click=self.__on_recalc_rollover)
            ]
        )

        self.__date_picker = ft.ElevatedButton(
            self.__start_date.format("MMM YYYY"),
            on_click=lambda e: self._page.open(
                ft.DatePicker(
                    current_date=self.__start_date,
                    on_change=self.__on_date_change
                )
            )
        )

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
                    icon=ft.Icons.CALENDAR_MONTH,
                    icon_color=ft.Colors.ON_PRIMARY_CONTAINER,
                    on_click=self.__on_current_month
                ),
                ft.IconButton(
                    icon=ft.Icons.ARROW_LEFT, on_click=self.__on_prev_month),
                self.__date_picker,
                ft.IconButton(
                    icon=ft.Icons.ARROW_RIGHT, on_click=self.__on_next_month),
                ft.VerticalDivider(
                    color=ft.Colors.ON_PRIMARY_CONTAINER,
                    leading_indent=5, trailing_indent=5),
                self.__income_total,
                self.__expense_total,
                self.__net_balance,
                ft.VerticalDivider(
                    color=ft.Colors.ON_PRIMARY_CONTAINER,
                    leading_indent=5, trailing_indent=5),
                # TODO: different view: Budget Progress | Calender | Itemized
                ft.SegmentedButton(
                    on_change=lambda evt: None,
                    selected={"itemized"},
                    segments=[
                        ft.Segment(icon=ft.Icon(ft.Icons.BAR_CHART, color=ft.Colors.ON_PRIMARY_CONTAINER), value="progress"),
                        ft.Segment(icon=ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.ON_PRIMARY_CONTAINER), value="calendar"),
                        ft.Segment(icon=ft.Icon(ft.Icons.FORMAT_LIST_BULLETED, color=ft.Colors.ON_PRIMARY_CONTAINER), value="itemized")
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


    def __layout_dlg(self):
        self.__confirm_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please Confirm"),
            content=ft.Text("PLACEHOLDER"),
            actions=[
                ft.TextButton("Yes", on_click=self.__on_delete),
                ft.TextButton("No", on_click=self.__on_delete),
            ]
        )

        self._page.overlay.append(self.__confirm_dlg)


    def handle_keyboard_event(self, event):
        if event.ctrl or event.meta:
            if event.key == "F":
                self.__search_control.focus()
            elif event.key == "N":
                self.__on_new(None)
        elif event.key in ("Arrow Up", "Arrow Down"):
            self.__editor.handle_keyboard_event(event)
