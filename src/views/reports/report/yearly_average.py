import flet as ft

import utils.tools
import utils.constants as const
from utils.locale import Locale
from models.expense import Expense

from views.reports.report.base import ReportBase

class YearlyAvgReport(ReportBase):
    def __init__(self, page):
        self.__curr_date = Locale.now()
        super().__init__(page)

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

        expenses = Expense.find(
            date=f"btw:{start_date.int_timestamp}:{end_date.int_timestamp}"
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
                    "total": exp.amount
                }
            else:
                data[exp.category]["total"] += exp.amount

        # Convert into list sorted by type, then category
        data = sorted(
            data.values(),
            key=lambda item: (item["type"], item["category"])
        )

        return data


    def render(self):
        self.__list_view.controls.clear()

        now = Locale.now()
        start_date = self.__curr_date.floor("year")
        months = 12 if start_date.year < now.year else now.month

        data = self.__load_data()
        for idx, item in enumerate(data):
            inc_color = utils.tools.cycle(const.INCOME_COLORS, idx)
            exp_color = utils.tools.cycle(const.EXPENSE_COLORS, idx)

            bgcolor = inc_color if item["type"] == Expense.TYPE_INCOME else exp_color

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
                            f"{Locale.currency(item["total"] / months)} / month",
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=2),
                        ft.Text(
                            Locale.currency(item["total"]),
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=2),
                    ]
                ),
                bgcolor=bgcolor
            )

            self.__list_view.controls.append(tile)

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
        with open(report_file, "w") as fptr:
            fptr.write(header)
            for item in data:
                avg = Locale.currency(item["total"] / months)
                total = Locale.currency(item["total"])
                line = f"| {item['category']} | {avg} / month | {total}\n"
                fptr.write(line)

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

        self._actions.extend([
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
