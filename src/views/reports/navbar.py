import flet as ft

import utils.constants as const

class ReportNavBar(ft.AppBar):
    def __init__(self, page, callbacks):
        self.__page = page

        self.__on_report_home = callbacks.get("report_home")

        self.__default_actions = [
            ft.IconButton(
                icon=ft.Icons.HOME,
                icon_color=ft.Colors.ON_PRIMARY_CONTAINER,
                on_click=self.__on_report_home
            ),
        ]

        super().__init__(
            leading=ft.Icon(
                ft.Icons.INSERT_CHART_OUTLINED, size=const.ICON_MEDIUM),
            title=ft.Text("Report - All"),
            bgcolor=ft.Colors.PRIMARY_CONTAINER,
            actions=self.__default_actions.copy()
        )


    def reset_actions(self):
        self.actions = self.__default_actions.copy()


    def set_title(self, title):
        self.title.value = f"Reports - {title}"
        self.title.update()
