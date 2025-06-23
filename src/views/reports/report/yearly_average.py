import flet as ft

import utils.tools
import utils.constants as const
from utils.locale import Locale
from models.budget import Budget
from models.expense import Expense

from views.reports.report.base import ReportBase

class YearlyAvgReport(ReportBase):
    def __init__(self, page):
        self.__curr_date = Locale.now()
        super().__init__(page)

        self.__init_header()
        self.__init_footer()

        self.__list_view = ft.ListView()
        self.content = self.__list_view


    @property
    def icon(self):
        return ft.Icon(ft.Icons.CALENDAR_MONTH)


    @property
    def name(self):
        return "Yearly Averages"


    @property
    def description(self):
        return "Income & Expense Totals for the Year with the Monthly Averages."


    def __load_data(self):
        start_date = self.__curr_date.floor("year")
        end_date = self.__curr_date.ceil("year")

        budget = Budget.group(Budget.find(deleted_at="null"))

        filters = {}
        if self.__search_control.value:
            filters["category"] = self.__search_control.value

        expenses = Expense.find(
            op="and",
            date=f"btw:{start_date.int_timestamp}:{end_date.int_timestamp}",
            **filters
        )

        data = {}
        # collect/munge/collate data
        for exp in expenses:
            if exp.category.startswith("Sixpence:"):
                continue

            if exp.category not in data:
                data[exp.category] = {
                    "type": exp.type,
                    "icon": exp.icon,
                    "category": exp.category,
                    "total": exp.amount,
                    "budget_group": budget.get(exp.category)
                }
            else:
                data[exp.category]["total"] += exp.amount

        # Convert into list sorted by type, then category
        data = sorted(
            data.values(),
            key=lambda item: (item["type"], item["category"])
        )

        return data


    def __init_header(self):
        self.__header = ft.ListTile(
            leading=ft.Icon(ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT),
            trailing=ft.Icon(ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT),
            title=ft.Row([
                ft.Text("Category",
                    color="black",
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                    weight=ft.FontWeight.BOLD,
                    expand=3),
                ft.Text(
                    "Monthly Average",
                    color="black",
                    weight=ft.FontWeight.BOLD,
                    expand=2),
                ft.Text(
                    "Total",
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

        self.__expenses_ctl = ft.Text(
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
                    expand=4),
                self.__income_ctl,
                self.__expenses_ctl,
                self.__diff_ctl

            ]),
            bgcolor=ft.Colors.GREY_300
        )


    def render(self):
        self.__list_view.controls.clear()

        # Header
        self.__list_view.controls.append(self.__header)

        now = Locale.now()
        start_date = self.__curr_date.floor("year")
        months = 12 if start_date.year < now.year else now.month

        income_amount = 0.0
        expense_amount = 0.0

        data = self.__load_data()
        for idx, item in enumerate(data):
            inc_color = utils.tools.cycle(const.INCOME_COLORS, idx)
            inc_color_alt = utils.tools.cycle(const.INCOME_COLORS, idx+1)
            exp_color = utils.tools.cycle(const.EXPENSE_COLORS, idx)
            exp_color_alt = utils.tools.cycle(const.EXPENSE_COLORS, idx+1)

            if item["type"] == Expense.TYPE_INCOME:
                bgcolor = inc_color
                income_amount += item["total"]
            else:
                bgcolor = exp_color
                expense_amount += item["total"]

            # add|remove|check_circle
            # add_box | upload
            trailing = None
            trailing_color = None
            budget_group = item["budget_group"]
            if budget_group:
                icon = ft.Icons.CHECK_CIRCLE
                trailing_color = inc_color_alt
                tooltip = "On Track"

                monthly_avg = abs(round(item["total"] / months, 2))
                # TODO:
                # - needs to take into account the freq of each item in the grp
                # - should be a monthly average not just a total
                budget_amt = abs(budget_group.amount)
                if monthly_avg != budget_amt:
                    icon = ft.Icons.ARROW_CIRCLE_UP

                    if monthly_avg > budget_amt:
                        trailing_color = exp_color_alt

                    tooltip = f"Update Budget ({monthly_avg} != {budget_group.amount})"

                # TODO: on_click
                # - how to deal with category with multiple items
                # - which item in group gets updated?
                trailing = ft.IconButton(
                    icon=icon,
                    icon_color=trailing_color,
                    tooltip=tooltip
                    # TODO: on_click
                )
            else:
                trailing = ft.IconButton(
                    icon=ft.Icons.ADD_BOX,
                    tooltip="Add To Budget"
                    # TODO: on_click
                )

            tile = ft.ListTile(
                leading=ft.Icon(item["icon"], color="black"),
                trailing=trailing,
                title=ft.Row(
                    [
                        ft.Text(item["category"],
                            color="black",
                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                            weight=ft.FontWeight.BOLD,
                            expand=3),
                        ft.Text(
                            f"{Locale.currency(item["total"] / months)} / month",
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=2),
                        ft.Text(
                            Locale.currency(item["total"]),
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=2)
                    ]
                ),
                bgcolor=bgcolor
            )

            self.__list_view.controls.append(tile)

        # Footer
        self.__income_ctl.value = "Income: " + Locale.currency(income_amount)
        self.__expenses_ctl.value = "Expenses: "+ Locale.currency(expense_amount)
        self.__diff_ctl.value = "Difference: " + Locale.currency(income_amount + expense_amount)
        self.__list_view.controls.append(self.__footer)

        self._page.update()


    def __on_year_display_click(self, evt):
        self.__curr_date = Locale.now()
        self.__year_display.label.value = self.__curr_date.year
        self.__year_display.update()

        self.render()


    def __on_change_year(self, evt):
        delta = evt.control.data
        self.__curr_date = self.__curr_date.shift(years=delta)
        self.__year_display.label.value = self.__curr_date.year
        self.__year_display.update()

        self.render()


    def __on_search_submit(self, evt):
        self.render()
        self.__search_control.focus()


    def _on_export(self, evt):
        export_path = evt.path
        data = self.__load_data()

        now = Locale.now()
        start_date = self.__curr_date.floor("year")
        curr_year = start_date.format('YYYY')
        months = 12 if start_date.year < now.year else now.month

        header = f"""
# Sixpence Report :: Yearly Averages
* **Year**: {curr_year}

--------------------------------------------------------------------------------

| Category   | Monthly Average | Total|
| ---------- | --------------- | ---- |
"""

        report_file = f"{export_path}/sixpence-report_yearly-avg-{curr_year}.md"
        inc_total = 0.0
        exp_total = 0.0
        with open(report_file, "w") as fptr:
            fptr.write(header)
            for item in data:
                avg = Locale.currency(item["total"] / months)
                total = Locale.currency(item["total"])
                line = f"| {item['category']} | {avg} / month | {total}\n"

                if item["type"] == Expense.TYPE_INCOME:
                    inc_total += item["total"]
                else:
                    exp_total += item["total"]

                fptr.write(line)

            # footer
            diff_total = Locale.currency(inc_total + exp_total)
            inc_total = Locale.currency(inc_total)
            exp_total = Locale.currency(exp_total)
            footer = f"""
| Income | Expenses | Difference |
| ------ | -------- | --- |
| {inc_total} | {exp_total} | {diff_total} |
"""
            fptr.write(footer)

        self._page.session.get("notification_bar").notify(
            ft.Icons.SAVE_ALT,
            f"Report Exported: {report_file}"
        )

    def _init_actions(self):
        super()._init_actions()

        self.__year_display = ft.Chip(
            ft.Text(self.__curr_date.year),
            on_click=self.__on_year_display_click
        )

        self.__search_control = ft.TextField(
            label="Category",
            prefix_icon=ft.Icons.SEARCH,
            on_submit=self.__on_search_submit)

        self._actions.extend([
            self.__search_control,
            ft.IconButton(
                icon=ft.Icons.ARROW_LEFT,
                icon_color=ft.Colors.ON_PRIMARY_CONTAINER,
                data=-1,
                on_click=self.__on_change_year
            ),
            self.__year_display,
            ft.IconButton(
                icon=ft.Icons.ARROW_RIGHT,
                icon_color=ft.Colors.ON_PRIMARY_CONTAINER,
                data=1,
                on_click=self.__on_change_year
            ),
        ])
