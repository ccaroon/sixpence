import flet as ft

from views.base import Base as BaseView
from views.reports.navbar import ReportNavBar

from views.reports.report.yearly_average import YearlyAvgReport

class ReportView(BaseView):
    def _layout(self):
        self.__reports = ft.GridView(
            runs_count=3,
            max_extent=265,
            child_aspect_ratio=1.75
        )
        self.content = self.__reports

        self.__yearly_avg = YearlyAvgReport()

        for report in (self.__yearly_avg,):
            self.__reports.controls.append(
                ft.Card(
                    ft.ListTile(
                        leading=report.icon,
                        title=ft.Text(report.name, weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(report.description),
                        data=report,
                        on_click=self.__on_report_click
                    )
                )
            )


    def __on_report_click(self, evt):
        report = evt.control.data
        self._navbar.set_title(report.name)
        self.content = report
        self.update()


    def __on_report_home(self, evt):
        self._navbar.set_title("All")
        self.content = self.__reports
        self.update()


    def _layout_navbar(self):
        self._navbar = ReportNavBar(
            self._page,
            callbacks={
                "report_home": self.__on_report_home
            }
        )
