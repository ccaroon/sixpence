import flet as ft

import utils.tools
from utils.locale import Locale
import utils.constants as const

from models.budget import Budget
from models.expense import Expense

class Expenses:
    VIEW_PROGRESS = "progress"
    VIEW_CALENDAR = "calendar"
    VIEW_ITEMIZED = "itemized"

    def __init__(self, view):
        now = Locale.now()

        self.__view = view

        self.__curr_date = now.floor("month")
        self.__curr_view = self.VIEW_PROGRESS

        self.__filters = self.__default_search_filters()

        Expense.update_rollover(now)


    @property
    def current_date(self):
        return self.__curr_date


    def __default_search_filters(self):
        end_date = self.__curr_date.ceil("month")
        return {
            "date": f"btw:{self.__curr_date.int_timestamp}:{end_date.int_timestamp}"
        }


    def handle_filter_by_tag(self, evt):
        self.refresh(
            tags=evt.control.label.value
        )


    def handle_edit(self, evt):
        expense = evt.control.data
        self.__view.editor.edit(expense, self.__budget, self.__categories)


    def handle_new(self, evt):
        expense = Expense(
            date=Locale.now()
        )
        self.__view.editor.edit(expense, self.__budget, self.__categories)


    def handle_delete(self, evt):
        self.__view._page.close(self.__view.confirm_dlg)

        if evt.control.text == "Yes":
            expense = self.__view.confirm_dlg.data
            expense.delete()
            self.refresh()


    def handle_delete_confirm(self, evt):
        item = evt.control.data

        self.__view.confirm_dlg.content = ft.Column(
            [
                ft.Text("Are you sure you want to delete this Expense?"),
                ft.Text(
                    f"{item.date.format("MMM DD, YYYY")} | {item.category} | {Locale.currency(item.amount)}?",
                    weight=ft.FontWeight.BOLD
                )
            ],
            tight=True
        )

        self.__view.confirm_dlg.data = item
        self.__view._page.open(self.__view.confirm_dlg)


    def handle_tile_click(self, evt):
        self.__view._navbar.change_view(self.VIEW_ITEMIZED)
        self.refresh(
            reset_filters=True,
            view=self.VIEW_ITEMIZED,
            category=evt.control.data
        )


    def refresh(self, **kwargs):
        reset_filters = kwargs.pop("reset_filters", False)

        view_opts = kwargs.pop("view_opts", {})

        if view := kwargs.pop("view", None):
            self.__curr_view = view

        self.__view.list_view.controls.clear()

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

        bdg_filters = {}
        if "category" in self.__filters:
            bdg_filters["category"] = self.__filters["category"]

        self.__categories = Budget.categories()
        self.__budget = Budget.for_month(
            self.__curr_date.month,
            **bdg_filters
        )

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

        self.__view._navbar.income_total = inc_total
        self.__view._navbar.expense_total = exp_total
        net_balance = inc_total + exp_total
        self.__view._navbar.net_balance = net_balance

        match self.__curr_view:
            case self.VIEW_ITEMIZED:
                self.__view_itemized(expenses)
            case self.VIEW_CALENDAR:
                self.__view_calendar(expenses)
            case self.VIEW_PROGRESS:
                budgeted, unbudgeted = self.__collate_progress_data(
                    expenses, **view_opts)
                self.__view_progress(budgeted, unbudgeted)
            case _:
                pass

        self.__view._page.update()


    def set_month(self, date):
        self.__curr_date = date.floor("month")
        end_date = date.ceil("month")

        self.__view._navbar.set_date_display(self.__curr_date.format("MMM YYYY"))

        self.__budget = Budget.for_month(self.__curr_date.month)
        self.refresh(
            date=f"btw:{self.__curr_date.int_timestamp}:{end_date.int_timestamp}"
        )


    def handle_month_change(self, evt):
        if isinstance(evt.control, ft.DatePicker):
            chosen_date = Locale.as_arrow(evt.control.value)
            self.set_month(chosen_date)
        else:
            offset = evt.control.data.get("offset", 0)
            # current month
            if offset == 0:
                self.set_month(Locale.now())
            # month + offset
            else:
                new_month = self.__curr_date.shift(months=offset)
                self.set_month(new_month)


    def __collate_progress_data(self, expenses, **kwargs):
        only_overbudget = kwargs.get("over_budget", False)
        only_zero_spent = kwargs.get("zero_spent", False)

        # BUDGETED ITEMS
        # Collate budget items by category & sum amounts
        budgeted = Budget.collate_by_category(self.__budget)

        # UNBUDGETED ITEMS
        # Collate unbudgeted items
        unbudgeted = {
            "items": {},
            "inc_total": 0.0,
            "exp_total": 0.0
        }
        for exp in expenses:
            if exp.category == Expense.ROLLOVER_CATEGORY:
                continue

            if exp.category in budgeted:
                budgeted[exp.category]["spent"] += exp.amount
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
        budgeted = sorted(
            budgeted.values(),
            key=lambda item: (item["type"], item["category"])
        )

        # Additional budgeted items filtering
        if only_zero_spent:
            budgeted = filter(lambda item: abs(item["spent"]) == 0.0, budgeted)
        elif only_overbudget:
            budgeted = filter(lambda item: abs(item["spent"]) > abs(item["amount"]), budgeted)

        # Convert into list sorted by type, then category
        unbudgeted["items"] = sorted(
            unbudgeted["items"].values(),
            key=lambda item: (item["type"], item["category"])
        )

        return (budgeted, unbudgeted)


    def __view_calendar(self, expenses):
        placeholder = ft.ListTile(ft.Text("CALENDAR VIEW NOT IMPLEMENTED"))
        self.__view.list_view.controls.append(placeholder)


    def __view_progress(self, budgeted, unbudgeted):
        self.__view.list_view.spacing = 4

        for item in budgeted:
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
                on_click=self.handle_tile_click
            )

            self.__view.list_view.controls.append(tile)

        # UNBUDGETED ITEMS
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
        self.__view.list_view.controls.append(unbudgeted_tile)

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
                on_click=self.handle_tile_click
            )
            unbudgeted_tile.controls.append(tile)


    def __view_itemized(self, expenses):
        self.__view.list_view.spacing = 0

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
                        on_click=self.handle_filter_by_tag,
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
                            on_click=self.handle_edit,
                            disabled=item.deleted_at is not None,
                        ),
                        ft.IconButton(ft.Icons.DELETE_FOREVER,
                            data=item,
                            icon_color=ft.Colors.GREY_500 if item.deleted_at else ft.Colors.GREY_800,
                            on_click=self.handle_delete_confirm,
                            disabled=item.deleted_at is not None
                        )
                    ],
                ),
                subtitle=ft.Text(
                    item.date.format("MMM DD, YYYY"),
                    color="black"),
                bgcolor=bgcolor
            )

            self.__view.list_view.controls.append(tile)
