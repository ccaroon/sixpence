import flet as ft

import utils.tools
import utils.constants as const
from utils.locale import Locale
from models.expense import Expense

class YearlyAvgReport(ft.Container):
    def __init__(self, page):
        self.__curr_date = Locale.now()
        self.__page = page
        super().__init__()

        self.__init_actions()

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
        return "List of each Income/Expense Category with the Monthly Average and Total Spent for the Year."


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


    def refresh(self):
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

        self.__page.update()


    def __on_year_display_click(self, evt):
        self.__curr_date = Locale.now()
        self.__year_display.label.value = self.__curr_date.year
        self.__year_display.update()

        self.refresh()


    def __on_change_year(self, evt):
        delta = evt.control.data
        self.__curr_date = self.__curr_date.shift(years=delta)
        self.__year_display.label.value = self.__curr_date.year
        self.__year_display.update()

        self.refresh()


    def __on_export(self, evt):
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

        self.__page.session.get("notification_bar").notify(
            ft.Icons.SAVE_ALT,
            f"Report Exported: {report_file}"
        )

    def __init_actions(self):
        self.__year_display = ft.Chip(
            ft.Text(self.__curr_date.year),
            on_click=self.__on_year_display_click
        )

        file_picker = ft.FilePicker(
            on_result=self.__on_export
        )
        self.__page.overlay.append(file_picker)

        self.__actions = [
            ft.VerticalDivider(),
            ft.IconButton(
                icon=ft.Icons.SAVE_ALT,
                icon_color=ft.Colors.ON_PRIMARY_CONTAINER,
                on_click=lambda _: file_picker.get_directory_path(),
                tooltip="Export"
            ),
            ft.VerticalDivider(),
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
        ]


    def actions(self):
        return self.__actions
