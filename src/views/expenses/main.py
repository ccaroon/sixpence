import flet as ft

import pprint

from models.budget import Budget
from models.expense import Expense

import utils.tools
from utils.locale import Locale
import utils.constants as const

from views.base import Base as BaseView
from views.expenses.editor import ExpenseEditor
from views.expenses.navbar import ExpenseNavBar

class ExpenseView(BaseView):

    VIEW_PROGRESS = "progress"
    VIEW_CALENDAR = "calendar"
    VIEW_ITEMIZED = "itemized"

    def __init__(self, page):
        now = Locale.now()
        self.__curr_date = now.floor("month")
        self.__curr_view = self.VIEW_PROGRESS

        Expense.update_rollover(now)

        self.__filters = self.__default_search_filters()
        self.__budget = Budget.for_month(self.__curr_date.month)
        self.__editor = ExpenseEditor(page, on_save=self._update)

        super().__init__(page)


    @property
    def current_date(self):
        return self.__curr_date


    def __on_tile_click(self, evt):
        self._navbar.change_view(self.VIEW_ITEMIZED)
        self._update(
            reset_filters=True,
            view=self.VIEW_ITEMIZED,
            category=evt.control.data
        )


    def __view_calendar(self, expenses):
        placeholder = ft.ListTile(ft.Text("CALENDAR VIEW NOT IMPLEMENTED"))
        self.__list_view.controls.append(placeholder)


    def __view_progress(self, expenses):
        self.__list_view.spacing = 4

        # BUDGETED ITEMS
        # Collate budget items by category & sum amounts
        budget = {}
        for item in self.__budget:
            if item.category not in budget:
                budget[item.category] = {
                    "type": item.type,
                    "icon": item.icon,
                    "category": item.category,
                    "amount": item.amount,
                    "spent": 0.0
                }
            else:
                budget[item.category]["amount"] += item.amount

        # Update amount spent for each category
        # Collate unbudgeted items
        unbudgeted = {
            "items": {},
            "inc_total": 0.0,
            "exp_total": 0.0
        }
        for exp in expenses:
            if exp.category == Expense.ROLLOVER_CATEGORY:
                continue

            if exp.category in budget:
                budget[exp.category]["spent"] += exp.amount
            else:
                if exp.category not in unbudgeted["items"]:
                    unbudgeted["items"][exp.category] = {
                        "type": exp.type,
                        "icon": exp.icon,
                        "category": exp.category,
                        "spent": exp.amount,
                        "count": 1
                    }
                else:
                    unbudgeted["items"][exp.category]["spent"] += exp.amount
                    unbudgeted["items"][exp.category]["count"] += 1

                if exp.type == Expense.TYPE_INCOME:
                    unbudgeted["inc_total"] += exp.amount
                elif exp.type == Expense.TYPE_EXPENSE:
                    unbudgeted["exp_total"] += exp.amount

        # Convert into list sorted by type, then category
        budget = sorted(
            budget.values(),
            key=lambda item: (item["type"], item["category"])
        )

        for item in budget:
            bgcolor = ft.Colors.WHITE if item["spent"] == 0.0 else ft.Colors.GREY_200
            progress_percent = round(item["spent"]/item["amount"], 2)
            percent_display = round(abs(progress_percent) * 100.00)

            progress_color = const.COLOR_INCOME
            if progress_percent > .9 and progress_percent < 1.0:
                progress_color = ft.Colors.YELLOW
            if progress_percent > 1.0:
                progress_color = const.COLOR_EXPENSE

            tile = ft.ListTile(
                leading=ft.Icon(item["icon"], color="black"),
                title=ft.Row(
                    [
                        ft.Text(item["category"],
                            color="black",
                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                            weight=ft.FontWeight.BOLD,
                            expand=3),
                        ft.Text(
                            f"{Locale.currency(item['spent'])} / {Locale.currency(item['amount'])}",
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=2),
                        ft.ProgressBar(
                            height=25,
                            color=progress_color,
                            bgcolor=ft.Colors.GREY_100,
                            value=progress_percent,
                            expand=5,
                        ),
                        ft.Text(
                            f"{percent_display}%",
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=1),
                    ],
                ),
                bgcolor=bgcolor,
                data=item["category"],
                on_click=self.__on_tile_click
            )

            self.__list_view.controls.append(tile)

        # UN-BUDGETED ITEMS
        # Convert into list sorted by type, then category
        unbudgeted["items"] = sorted(
            unbudgeted["items"].values(),
            key=lambda item: (item["type"], item["category"])
        )

        # Tile for main list
        unbudgeted_tile = ft.ExpansionTile(
            leading=ft.Icon(ft.Icons.HELP_CENTER),
            title=ft.Row(
                [
                    ft.Text("Unbudgeted",
                        color="black",
                        theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                        weight=ft.FontWeight.BOLD,
                        expand=3
                    ),
                    ft.Text(Locale.currency(unbudgeted["inc_total"]),
                        color=const.COLOR_INCOME,
                        theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                        weight=ft.FontWeight.BOLD,
                        expand=2
                    ),
                    ft.Text(Locale.currency(unbudgeted["exp_total"]),
                        color=const.COLOR_EXPENSE,
                        theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                        weight=ft.FontWeight.BOLD,
                        expand=6
                    ),
                ]
            ),
            icon_color=ft.Colors.LIGHT_GREEN_ACCENT_400,
            collapsed_icon_color=ft.Colors.RED,
            bgcolor=ft.Colors.GREY_300,
            collapsed_bgcolor=ft.Colors.GREY_300,
            maintain_state=True,
        )
        self.__list_view.controls.append(unbudgeted_tile)

        # Add tiles to expansion tile
        for idx, item in enumerate(unbudgeted["items"]):
            inc_color = utils.tools.cycle(const.INCOME_COLORS, idx)
            exp_color = utils.tools.cycle(const.EXPENSE_COLORS, idx)
            bgcolor = exp_color if item["type"] == Expense.TYPE_EXPENSE else inc_color

            tile = ft.ListTile(
                leading=ft.Icon(item["icon"], color="black"),
                title=ft.Row(
                    [
                        ft.Text(item["category"],
                            color="black",
                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                            weight=ft.FontWeight.BOLD,
                            expand=3),
                        ft.Text(
                            f"{Locale.currency(item['spent'])}",
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=2),
                        ft.Text(
                            item["count"],
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=6),
                    ],
                ),
                bgcolor=bgcolor,
                data=item["category"],
                on_click=self.__on_tile_click
            )
            unbudgeted_tile.controls.append(tile)


    def __view_itemized(self, expenses):
        self.__list_view.spacing = 0

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
            else:
                bgcolor = exp_color
                tag_color = exp_color_alt

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


    def _update(self, **kwargs):
        reset_filters = kwargs.pop("reset_filters", False)

        if view := kwargs.pop("view", None):
            self.__curr_view = view

        self.__list_view.controls.clear()

        if reset_filters:
            self.__filters = self.__default_search_filters()

        # From here, kwargs is assumed to be search filters. Other options
        # have been removed.
        # Value of 'None' == delete from filters
        for fld, value in kwargs.items():
            if value is None:
                del self.__filters[fld]
            else:
                self.__filters[fld] = value

        # pprint.pprint(f"Filters: [{self.__filters}]")
        expenses = Expense.find(
            op="and",
            sort_by="type,date",
            **self.__filters
        )

        inc_total = 0.0
        exp_total = 0.0
        for exp in expenses:
            if exp.type == Expense.TYPE_INCOME:
                inc_total += exp.amount
            elif exp.type == Expense.TYPE_EXPENSE:
                exp_total += exp.amount

        self._navbar.income_total = inc_total
        self._navbar.expense_total = exp_total
        net_balance = inc_total + exp_total
        self._navbar.net_balance = net_balance

        match self.__curr_view:
            case self.VIEW_ITEMIZED:
                self.__view_itemized(expenses)
            case self.VIEW_CALENDAR:
                self.__view_calendar(expenses)
            case self.VIEW_PROGRESS:
                self.__view_progress(expenses)
            case _:
                pass

        self._page.update()


    def _layout(self):
        self.__list_view = ft.ListView()
        self.content = self.__list_view
        self.__layout_dlg()
        self._update()


    def _layout_navbar(self):
        self._navbar = ExpenseNavBar(
            self._page,
            parent=self,
            callbacks={
                "on_refresh": self._update,
                "on_new": self.__on_new,
                "on_change_month": self.__on_change_month
            }
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


    def __default_search_filters(self):
        end_date = self.__curr_date.ceil("month")
        return {
            "date": f"btw:{self.__curr_date.int_timestamp}:{end_date.int_timestamp}"
        }


    def __filter_by_tag(self, evt):
        self._update(
            tags=evt.control.label.value
        )


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


    def __set_month(self, date):
        self.__curr_date = date.floor("month")
        end_date = date.ceil("month")

        self._navbar.set_date_display(self.__curr_date.format("MMM YYYY"))

        self.__budget = Budget.for_month(self.__curr_date.month)
        self._update(
            date=f"btw:{self.__curr_date.int_timestamp}:{end_date.int_timestamp}"
        )


    def __on_change_month(self, evt):
        if isinstance(evt.control, ft.DatePicker):
            chosen_date = Locale.as_arrow(evt.control.value)
            self.__set_month(chosen_date)
        else:
            offset = evt.control.data.get("offset", 0)
            # current month
            if offset == 0:
                self.__set_month(Locale.now())
            # month + offset
            else:
                new_month = self.__curr_date.shift(months=offset)
                self.__set_month(new_month)


    def handle_keyboard_event(self, event):
        if event.ctrl or event.meta:
            if event.key == "F":
                self._navbar.handle_keyboard_event(event)
            elif event.key == "N":
                self.__on_new(None)
        elif event.key in ("Arrow Up", "Arrow Down"):
            self.__editor.handle_keyboard_event(event)
