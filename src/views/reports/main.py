import flet as ft

from presenters.reports import Reports as ReportPresenter

from views.base import Base as BaseView
from views.reports.navbar import ReportNavBar

from views.reports.report.spending import SpendingReport
from views.reports.report.yearly_average import YearlyAvgReport
from views.reports.report.upcoming import UpcomingReport

class Report(BaseView):
    def __init__(self, page):
        super().__init__(page, ReportPresenter(self))

        reports = [
            SpendingReport(page),
            UpcomingReport(page),
            YearlyAvgReport(page)
        ]

        for report in reports:
            self.reports.controls.append(
                ft.Card(
                    ft.ListTile(
                        leading=report.icon,
                        title=ft.Text(report.name, weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(report.description),
                        data=report,
                        on_click=self._presenter.handle_report_click
                    )
                )
            )


    def _layout(self):
        self.reports = ft.GridView(
            runs_count=3,
            max_extent=265,
            child_aspect_ratio=1.75
        )
        self.content = self.reports


    def _layout_navbar(self):
        self._navbar = ReportNavBar(
            self._page,
            callbacks={
                "report_home": self._presenter.handle_report_home
            }
        )
