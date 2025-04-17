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

        self.__init_actions()
        self.__init_header()
        self.__init_footer()

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
        return "What you've been spending your money on a given period of time."


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
                    expand=2),
                ft.Text(
                    "Count",
                    color="black",
                    weight=ft.FontWeight.BOLD,
                    expand=2),
                ft.Text(
                    "Average",
                    color="black",
                    weight=ft.FontWeight.BOLD,
                    expand=2),
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

        self.__net_ctl = ft.Text(
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
                self.__net_ctl

            ]),
            bgcolor=ft.Colors.GREY_300
        )


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
                    "amount": exp.amount,
                    "count": 1
                }
            else:
                data[exp.category]["amount"] += exp.amount
                data[exp.category]["count"] += 1

        # Convert into list sorted by type, then category
        data = sorted(
            data.values(),
            key=lambda item: (item["type"], item["category"])
        )

        return data


    def render(self):
        self.__list_view.controls.clear()

        # Header
        self.__list_view.controls.append(self.__header)

        income_amount = 0.0
        expense_amount = 0.0
        data = self.__load_data()
        for idx, item in enumerate(data):
            inc_color = utils.tools.cycle(const.INCOME_COLORS, idx)
            exp_color = utils.tools.cycle(const.EXPENSE_COLORS, idx)

            if item["type"] == Expense.TYPE_INCOME:
                bgcolor = inc_color
                income_amount += item["amount"]
            else:
                bgcolor = exp_color
                expense_amount += item["amount"]

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
                            expand=2),
                        ft.Text(
                            f"{item["count"]}x",
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=2),
                        ft.Text(
                            Locale.currency(item["amount"] / item["count"]),
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=2),
                    ]
                ),
                bgcolor=bgcolor
            )

            self.__list_view.controls.append(tile)

        # Footer
        self.__income_ctl.value = "Income: " + Locale.currency(income_amount)
        self.__expenses_ctl.value = "Expenses: "+ Locale.currency(expense_amount)
        self.__net_ctl.value = "Net: " + Locale.currency(income_amount + expense_amount)
        self.__list_view.controls.append(self.__footer)

        self.__page.update()


    def __on_export(self, evt):
        export_path = evt.path
        (start_date, end_date) = self.__date_range()

        start_disp = start_date.format("MMM DD, YYYY")
        end_disp = end_date.format("MMM DD, YYYY")

        inc_total = 0.0
        exp_total = 0.0

        data = self.__load_data()

        header = f"""
# Sixpence Report :: Spending
* **Period**: Last {self.__period} Days ({start_disp} to {end_disp})

--------------------------------------------------------------------------------

| Category | Amount | Count | Average |
| -------- | ------ | ----- | ------- |
"""

        report_file = f"{export_path}/sixpence-report_spending-{self.__period}.md"
        with open(report_file, "w") as fptr:
            # header
            fptr.write(header)

            # report data
            for item in data:
                if item["type"] == Expense.TYPE_INCOME:
                    inc_total += item["amount"]
                else:
                    exp_total += item["amount"]

                avg = Locale.currency(item["amount"] / item["count"])
                amount = Locale.currency(item["amount"])
                line = f"| {item['category']} | {amount} | {item['count']} | {avg} |\n"
                fptr.write(line)

            # footer
            net_total = Locale.currency(inc_total + exp_total)
            inc_total = Locale.currency(inc_total)
            exp_total = Locale.currency(exp_total)
            footer = f"""
| Income | Expenses | Net |
| ------ | -------- | --- |
| {inc_total} | {exp_total} | {net_total} |
"""
            fptr.write(footer)


        self.__page.session.get("notification_bar").notify(
            ft.Icons.SAVE_ALT,
            f"Report Exported: {report_file}"
        )


    def __on_time_period_change(self, evt):
        self.__period = int(list(evt.control.selected)[0])

        self.refresh()


    def __init_actions(self):
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

    def actions(self):
        return self.__actions
