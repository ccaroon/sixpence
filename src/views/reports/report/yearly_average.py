import flet as ft

class YearlyAvgReport(ft.Container):
    def __init__(self):
        super().__init__(
            ft.Text("Yearly Average Report")
        )


    @property
    def icon(self):
        return ft.Icon(ft.Icons.CALENDAR_MONTH)


    @property
    def name(self):
        return "Yearly Averages"


    @property
    def description(self):
        return "List of each Income/Expense Category with the Monthly Average and Total Spent for the Year."
