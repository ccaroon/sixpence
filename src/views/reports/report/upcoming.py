import flet as ft

import utils.tools
import utils.constants as const

from models.budget import Budget
from models.expense import Expense

from utils.locale import Locale

from views.reports.report.base import ReportBase

class UpcomingReport(ReportBase):
    def __init__(self, page):
        super().__init__(page)

        self.__init_header()
        self.__init_footer()

        self.__list_view = ft.ListView()
        self.content = self.__list_view


    @property
    def icon(self):
        return ft.Icon(ft.Icons.NEXT_PLAN)


    @property
    def name(self):
        return "Upcoming Income & Expenses"


    @property
    def description(self):
        return "Upcoming income & expenses for the current month."


    # def _init_actions(self):
    #     super()._init_actions()

    #     self._actions.extend([
    #         ft.Text("Hello, World!")
    #     ])


    def __init_header(self):
        self.__header = ft.ListTile(
            leading=ft.Icon(ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT),
            trailing=ft.Icon(ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT),
            title=ft.Row([
                ft.Text("Category",
                    color="black",
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                    weight=ft.FontWeight.BOLD,
                    expand=4),
                ft.Text(
                    "Amount",
                    color="black",
                    weight=ft.FontWeight.BOLD,
                    expand=2)
            ]),
            bgcolor=ft.Colors.GREY_300
        )


    def __init_footer(self):
        self.__income_ctl = ft.Text(
            "$0.00",
            color="black",
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
            weight=ft.FontWeight.BOLD,
            expand=2
        )
        self.__expense_ctl = ft.Text(
            "$0.00",
            color="black",
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
            weight=ft.FontWeight.BOLD,
            expand=2
        )

        self.__footer = ft.ListTile(
            leading=ft.Icon(ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT),
            trailing=ft.Icon(ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT),
            title=ft.Row([
                ft.Text("Grand Totals",
                    color="black",
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                    weight=ft.FontWeight.BOLD,
                    expand=2),
                self.__income_ctl,
                self.__expense_ctl

            ]),
            bgcolor=ft.Colors.GREY_300
        )


    def __load_data(self):
        now = Locale.now()
        start_date = now.floor("month")
        end_date = now.ceil("month")

        budget = Budget.for_month(now.month)
        budget_map = Budget.collate_by_category(budget)

        expenses = Expense.find(
            date=f"btw:{start_date.int_timestamp}:{end_date.int_timestamp}"
        )

        # collect/munge/collate data
        for exp in expenses:
            if exp.category in budget_map:
                if exp.type == Expense.TYPE_INCOME:
                    budget_map[exp.category]["amount"] -= exp.amount
                elif exp.type == Expense.TYPE_EXPENSE:
                    del budget_map[exp.category]

        # Convert into list sorted by type, then category
        data = sorted(
            budget_map.values(),
            key=lambda item: (item["type"], item["category"])
        )

        return data


    def render(self):
        self.__list_view.controls.clear()

        # Header
        self.__list_view.controls.append(self.__header)

        income_total = 0.0
        expense_total = 0.0
        data = self.__load_data()
        for idx, item in enumerate(data):
            inc_color = utils.tools.cycle(const.INCOME_COLORS, idx)
            exp_color = utils.tools.cycle(const.EXPENSE_COLORS, idx)

            if item["type"] == Expense.TYPE_INCOME:
                bgcolor = inc_color
                income_total += item["amount"]
            else:
                bgcolor = exp_color
                expense_total += item["amount"]

            tile = ft.ListTile(
                leading=ft.Icon(item["icon"], color="black"),
                title=ft.Row(
                    [
                        ft.Text(item["category"],
                            color="black",
                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                            weight=ft.FontWeight.BOLD,
                            expand=4),
                        ft.Text(
                            Locale.currency(item["amount"]),
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=2)
                    ]
                ),
                bgcolor=bgcolor
            )

            self.__list_view.controls.append(tile)

        # Footer
        self.__income_ctl.value = "Income: " + Locale.currency(income_total)
        self.__expense_ctl.value = "Expenses: " + Locale.currency(expense_total)
        self.__list_view.controls.append(self.__footer)

        self._page.update()


    def _on_export(self, evt):
        income_total = 0.0
        expense_total = 0.0
        now = Locale.now()

        data = self.__load_data()

        start_date = now.format("MMM-DD-YYYY")
        end_date = now.ceil('month').format("MMM-DD-YYYY")
        report_file = f"{evt.path}/sixpence-report_upcoming-{start_date}.md"

        header = f"""
# Sixpence Report :: Upcoming Income & Expenses
* **Date**: {start_date} to {end_date}
| Category | Amount |
| -------- | ------ |
"""

        with open(report_file, "w") as fptr:
            fptr.write(header)
            for item in data:
                if item["type"] == Expense.TYPE_EXPENSE:
                    expense_total += item["amount"]
                else:
                    income_total += item["amount"]

                fptr.write(f"| {item['category']} | {Locale.currency(item['amount'])} |\n")

            footer = f"""
| Totals | Income | Expenses |
| ------ | ------ | -------- |
|        | {Locale.currency(income_total)}     | {Locale.currency(expense_total)}       |
"""
            fptr.write(footer)


        self._page.session.get("notification_bar").notify(
            ft.Icons.SAVE_ALT,
            f"Report Exported: {report_file}"
        )
