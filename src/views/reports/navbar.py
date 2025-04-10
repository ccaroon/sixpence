import flet as ft

# import pprint
import utils.constants as const
# from utils.locale import Locale
# import utils.tools

class ReportNavBar(ft.AppBar):
    def __init__(self, page, callbacks):
        self.__page = page
        self.__on_report_home = callbacks.get("report_home")

        super().__init__(
            leading=ft.Icon(
                ft.Icons.INSERT_CHART_OUTLINED, size=const.ICON_MEDIUM),
            title=ft.Text("Report - All"),
            bgcolor=ft.Colors.PRIMARY_CONTAINER,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.HOME,
                    icon_color=ft.Colors.ON_PRIMARY_CONTAINER,
                    on_click=self.__on_report_home
                ),
            ]
        )


    def set_title(self, title):
        self.title.value = f"Reports - {title}"
        self.update()
