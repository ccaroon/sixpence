import flet as ft

import utils.tools
import utils.constants as const
from utils.locale import Locale
from models.budget import Budget
from models.expense import Expense

from views.reports.report.base import ReportBase

class YearlyAvgReport(ReportBase):

    STATUS_UNBUDGETED = "Unbudgeted"
    STATUS_ON_TRACK = "On Track"
    STATUS_OVER = "Over Budget"
    STATUS_UNDER = "Under Budget"

    def __init__(self, page):
        self.__report_date = Locale.now()
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


    def __load_data(self, start_date, end_date):
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
                    expand=2),
                ft.Text(
                    "Total",
                    color="black",
                    weight=ft.FontWeight.BOLD,
                    expand=1),
                ft.Text(
                    "Monthly Average",
                    color="black",
                    weight=ft.FontWeight.BOLD,
                    expand=1),
                ft.Text(
                    "Progress",
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

    def __collated_data(self):
        now = Locale.now()
        start_date = None
        end_date = None
        months = None
        if self.__report_date.year < now.year:
            start_date = self.__report_date.floor("year")
            end_date = self.__report_date.ceil("year")
            months = 12
        else:
            start_date = self.__report_date.floor("year")
            end_date = now.shift(months=-1).ceil("month")
            months = now.month - 1

        data = self.__load_data(start_date, end_date)
        for item in data:
            budget_group = item["budget_group"]
            item["bg_yearly_amt"] = 0.0
            item["status"] = self.STATUS_UNBUDGETED
            item["monthly_avg"] = item["total"] / months
            if budget_group:
                item["bg_yearly_amt"] = budget_group.amount_yearly

                # How much should have been spent by now (curr_month)
                predicted_spent = abs(budget_group.predict_spending(months))
                total_ytd = abs(item["total"])
                if total_ytd == predicted_spent:
                    item["status"] = self.STATUS_ON_TRACK
                elif total_ytd > predicted_spent:
                    item["status"] = self.STATUS_OVER
                elif total_ytd < predicted_spent:
                    item["status"] = self.STATUS_UNDER

        return data


    def render(self):
        self.__list_view.controls.clear()

        # Header
        self.__list_view.controls.append(self.__header)

        data = self.__collated_data()

        income_amount = 0.0
        expense_amount = 0.0

        for idx, item in enumerate(data):
            inc_color = utils.tools.cycle(const.INCOME_COLORS, idx)
            exp_color = utils.tools.cycle(const.EXPENSE_COLORS, idx)

            if item["type"] == Expense.TYPE_INCOME:
                bgcolor = inc_color
                income_amount += item["total"]
            else:
                bgcolor = exp_color
                expense_amount += item["total"]

            trailing = None
            trailing_color = None
            budget_group = item["budget_group"]
            bg_amount = item["bg_yearly_amt"]
            tooltip = item["status"]
            if budget_group:
                progress_value = item["total"] / bg_amount
                progress_color = ft.Colors.GREEN_ACCENT_200
                if progress_value > .9 and progress_value < 1.0:
                    progress_color = ft.Colors.YELLOW_ACCENT_200
                if progress_value > 1.0:
                    progress_color = ft.Colors.RED_ACCENT_200

                progress_control = ft.ProgressBar(
                    height=25,
                    value=progress_value,
                    tooltip=f"{Locale.currency(item["total"])} / {Locale.currency(bg_amount)}",
                    color=progress_color,
                    expand=2
                )

                # How much should have been spent by now (curr_month)
                if item["status"] == self.STATUS_ON_TRACK:
                    icon = ft.Icons.CHECK_BOX
                    trailing_color = ft.Colors.GREEN_ACCENT_200
                elif item["status"] == self.STATUS_OVER:
                    icon = ft.Icons.TRENDING_UP
                    trailing_color = ft.Colors.RED_ACCENT_200
                elif item["status"] == self.STATUS_UNDER:
                    icon = ft.Icons.TRENDING_DOWN
                    trailing_color = ft.Colors.GREEN_ACCENT_200

                trailing = ft.Icon(
                    icon,
                    color=trailing_color,
                    tooltip=tooltip
                )
            else:
                progress_control = ft.Text(
                    "-",
                    color="black",
                    weight=ft.FontWeight.BOLD,
                    expand=2)
                trailing = ft.Icon(ft.Icons.TRENDING_FLAT, tooltip=tooltip)

            tile = ft.ListTile(
                leading=ft.Icon(item["icon"], color="black"),
                trailing=trailing,
                title=ft.Row(
                    [
                        ft.Text(f"{item["category"]}",
                            color="black",
                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                            weight=ft.FontWeight.BOLD,
                            expand=2),
                        ft.Text(
                            Locale.currency(item["total"]),
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=1),
                        ft.Text(
                            f"{Locale.currency(item["monthly_avg"])} / month",
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=1),
                        progress_control,
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
        self.__report_date = Locale.now()
        self.__year_display.label.value = self.__report_date.year
        self.__year_display.update()

        self.render()


    def __on_change_year(self, evt):
        delta = evt.control.data
        self.__report_date = self.__report_date.shift(years=delta)
        self.__year_display.label.value = self.__report_date.year
        self.__year_display.update()

        self.render()


    def __on_search_submit(self, evt):
        self.render()
        self.__search_control.focus()


    def _on_export(self, evt):
        export_path = evt.path
        curr_year = self.__report_date.format('YYYY')
        data = self.__collated_data()

        header = f"""
# Sixpence Report :: Yearly Averages
* **Year**: {curr_year}

--------------------------------------------------------------------------------

| Category   | Total | Monthly Average | Progress | Status |
| ---------- | ----- | --------------- | -------- | ------ |
"""

        report_file = f"{export_path}/sixpence-report_yearly-avg-{curr_year}.md"
        inc_total = 0.0
        exp_total = 0.0
        with open(report_file, "w") as fptr:
            fptr.write(header)
            for item in data:
                budget_group = item["budget_group"]
                bg_amount = item["bg_yearly_amt"]
                progress = "-"
                if budget_group:
                    progress = f"{Locale.currency(item["total"])} / {Locale.currency(bg_amount)}"

                avg = Locale.currency(item["monthly_avg"])
                total = Locale.currency(item["total"])
                line = f"| {item['category']} | {total} | {avg} / month | {progress} | {item['status']}|\n"

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
            ft.Text(self.__report_date.year),
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
