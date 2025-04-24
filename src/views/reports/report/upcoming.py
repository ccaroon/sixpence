import flet as ft

import utils.tools
import utils.constants as const

from models.budget import Budget
from models.expense import Expense

from utils.locale import Locale

from views.reports.report.base import ReportBase

class UpcomingReport(ReportBase):
    def __init__(self, page):
        # In Weeks
        self.__period = 1

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


    def __compute_period(self):
        now = Locale.now()
        start = now.floor("day")
        end = now.shift(weeks=self.__period).ceil('day')

        return (start,end)


    def __update_date_display(self):
        start, end = self.__compute_period()

        start_date = start.format("MMM DD")
        end_date = end.format("MMM DD")
        self._date_display.label.value = f"{start_date} - {end_date}"


    def _init_actions(self):
        super()._init_actions()

        self._date_display = ft.Chip(
            leading=ft.Icon(ft.Icons.DATE_RANGE),
            label=ft.Text(""),
            on_click=lambda e: None
        )
        self.__update_date_display()

        self._actions.extend([
            ft.SegmentedButton(
                selected={self.__period},
                segments=[
                    ft.Segment(label=ft.Text("1w"), value=1),
                    ft.Segment(label=ft.Text("2w"), value=2),
                ],
                on_change=self.__on_time_period_change
            ),
            ft.VerticalDivider(),
            self._date_display
        ])


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


    def __on_time_period_change(self, evt):
        self.__period = int(list(evt.control.selected)[0])
        self.__update_date_display()
        self.render()


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
        self.__diff_ctl = ft.Text(
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
                self.__expense_ctl,
                self.__diff_ctl,

            ]),
            bgcolor=ft.Colors.GREY_300
        )


    def __load_data(self):
        now = Locale.now()

        # Start/End dates of define period
        # I.e. Start/End dates of last N weeks
        (period_start, period_end) = self.__compute_period()

        # Load this month's budget
        budget = Budget.for_month(now.month)
        budget_map = Budget.collate_by_category(budget)

        # Load expenses for current month
        start_date = now.floor("month")
        end_date = now.ceil("month")
        curr_expenses = Expense.find(
            date=f"btw:{start_date.int_timestamp}:{end_date.int_timestamp}"
        )
        curr_exp_map = Expense.collate_by_category(curr_expenses)

        # Load expenses from the period of LAST month
        # I.e. the last N weeks of LAST month
        start_date = period_start.shift(months=-1)
        end_date = start_date.shift(weeks=self.__period).ceil("day")
        period_expenses = Expense.find(
            date=f"btw:{start_date.int_timestamp}:{end_date.int_timestamp}"
        )
        period_exp_map = Expense.collate_by_category(period_expenses)

        # for each budgeted item
        # look for the category in expenses
        # if exists, then that item/category was paid in the given period last
        # month, so it is likey due in the coming period also
        data = []
        for category, item in budget_map.items():
            expected_amt = 0.0
            if category in period_exp_map:
                expected_items = period_exp_map[category]
                expected_amt = sum([item.amount for item in expected_items])

                # spent_amount = 0.0
                # if category in curr_exp_map:
                #     curr_items = curr_exp_map[category]
                #     spent_amount = sum([item.amount for item in curr_items])

                data.append({
                    "type": item["type"],
                    "icon": item["icon"],
                    "category": item["category"],
                    # "spent_amt": spent_amount,
                    "budget_amt": item["amount"],
                    # "expected_amt": item["amount"] - spent_amount
                    "expected_amt": expected_amt
                })

        # # Filter out items where budget amount (or more) has been spent
        # data = filter(lambda item: abs(item["spent_amt"]) < abs(item["budget_amt"]), data)

        # Convert into list sorted by type, then category
        data = sorted(
            data,
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
                income_total += item["expected_amt"]
            else:
                bgcolor = exp_color
                expense_total += item["expected_amt"]

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
                            Locale.currency(item["expected_amt"]),
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=2)
                    ]
                ),
                bgcolor=bgcolor
            )

            self.__list_view.controls.append(tile)

        # Footer
        self.__diff_ctl.value = "Difference: " + Locale.currency(income_total + expense_total)
        self.__income_ctl.value = "Income: " + Locale.currency(income_total)
        self.__expense_ctl.value = "Expenses: " + Locale.currency(expense_total)
        self.__list_view.controls.append(self.__footer)

        self._page.update()


    def _on_export(self, evt):
        income_total = 0.0
        expense_total = 0.0
        now = Locale.now()

        data = self.__load_data()

        start_date = now.floor("day").format("MMM-DD-YYYY")
        end_date = now.shift(weeks=self.__period).ceil('day').format("MMM-DD-YYYY")
        report_file = f"{evt.path}/sixpence-report_upcoming-{start_date}-{self.__period}w.md"

        header = f"""
# Sixpence Report :: Upcoming Income & Expenses
* **Date**: {start_date} to {end_date} (Next {self.__period} weeks)
| Category | Amount |
| -------- | ------ |
"""

        with open(report_file, "w") as fptr:
            fptr.write(header)
            for item in data:
                if item["type"] == Expense.TYPE_EXPENSE:
                    expense_total += item["expected_amt"]
                else:
                    income_total += item["expected_amt"]

                fptr.write(f"| {item['category']} | {Locale.currency(item['expected_amt'])} |\n")

            footer = f"""
| Totals | Income | Expenses | Difference |
| ------ | ------ | -------- | ---------- |
|        | {Locale.currency(income_total)} | {Locale.currency(expense_total)} | {Locale.currency(income_total + expense_total)} |
"""
            fptr.write(footer)


        self._page.session.get("notification_bar").notify(
            ft.Icons.SAVE_ALT,
            f"Report Exported: {report_file}"
        )
