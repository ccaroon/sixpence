import flet as ft

import utils.tools
import utils.constants as const
from utils.locale import Locale
from models.expense import Expense

class SpendingReport(ft.Container):
    def __init__(self, page):
        self.__period = 7
        self.__page = page

        super().__init__()

        self.__list_view = ft.ListView()
        self.content = self.__list_view


    @property
    def icon(self):
        return ft.Icon(ft.Icons.SELL)


    @property
    def name(self):
        return "Spending"


    @property
    def description(self):
        return "Display what you've been spending your money in a given period of time."


    def __date_range(self):
        end_date = Locale.now().ceil("day")
        start_date = end_date.shift(days=self.__period * -1).floor("day")

        return (start_date, end_date)


    def __load_data(self):
        (start_date, end_date) = self.__date_range()

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
                    "total": exp.amount,
                    "count": 1
                }
            else:
                data[exp.category]["total"] += exp.amount
                data[exp.category]["count"] += 1

        # Convert into list sorted by type, then category
        data = sorted(
            data.values(),
            key=lambda item: (item["type"], item["category"])
        )

        return data


    def refresh(self):
        self.__list_view.controls.clear()

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
                            Locale.currency(item["total"]),
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=2),
                        ft.Text(
                            f"{item["count"]}x",
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=2),
                        ft.Text(
                            Locale.currency(item["total"] / item["count"]) + " avg",
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=2),
                    ]
                ),
                bgcolor=bgcolor
            )

            self.__list_view.controls.append(tile)

        self.__page.update()


    def __on_export(self, evt):
        export_path = evt.path
        (start_date, end_date) = self.__date_range()

        start_disp = start_date.format("MMM DD, YYYY")
        end_disp = end_date.format("MMM DD, YYYY")

        data = self.__load_data()

        header = f"""# Sixpence Report
## Spending for the Last {self.__period} Days ({start_disp} to {end_disp})
| Category | Total | Count | Average |
| -------- | ----- | ----- | ------- |
"""

        report_file = f"{export_path}/sixpence-report-spending-{self.__period}.md"
        with open(report_file, "w") as fptr:
            fptr.write(header)
            for item in data:
                avg = Locale.currency(item["total"] / item["count"])
                total = Locale.currency(item["total"])
                line = f"| {item['category']} | {total} | {item['count']} | {avg} |\n"
                fptr.write(line)

        self.__page.session.get("notification_bar").notify(
            ft.Icons.SAVE_ALT,
            f"Report Exported: {report_file}"
        )


    def __on_time_period_change(self, evt):
        self.__period = int(list(evt.control.selected)[0])

        self.refresh()


    def actions(self):
        file_picker = ft.FilePicker(
            on_result=self.__on_export
        )
        self.__page.overlay.append(file_picker)

        return [
            ft.VerticalDivider(),
            ft.IconButton(
                icon=ft.Icons.SAVE_ALT,
                icon_color=ft.Colors.ON_PRIMARY_CONTAINER,
                on_click=lambda _: file_picker.get_directory_path(),
                tooltip="Export"
            ),
            ft.VerticalDivider(),
            ft.SegmentedButton(
                selected={7},
                segments=[
                    ft.Segment(label=ft.Text("7d"),  value=7),
                    ft.Segment(label=ft.Text("14d"), value=14),
                    ft.Segment(label=ft.Text("30d"), value=30),
                    ft.Segment(label=ft.Text("60d"), value=60),
                    ft.Segment(label=ft.Text("90d"), value=90)
                ],
                on_change=self.__on_time_period_change

            )
        ]
