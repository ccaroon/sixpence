import flet as ft

import utils.constants as const

class NavRail(ft.NavigationRail):

    def __init__(self, page):
        super().__init__(
            selected_index=0,
            # leading=ft.Image(src="../assets/logo.png"),
            height=999,
            expand=1,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icons.HOME,
                    label="Home"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.FORMAT_LIST_BULLETED_OUTLINED,
                    selected_icon=ft.Icons.FORMAT_LIST_BULLETED,
                    label="Budget"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.ATTACH_MONEY_OUTLINED,
                    selected_icon=ft.Icons.ATTACH_MONEY,
                    label="Expenses",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.INSERT_CHART_OUTLINED,
                    selected_icon=ft.Icons.INSERT_CHART,
                    label="Reports",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="Settings",
                ),
            ],
            on_change=self.__handle_on_change
        )

        self.__page = page

        if self.__page.session.get("config").get("session:env") != "prod":
            self.destinations.append(
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.LOGO_DEV, color="red", size=const.ICON_MEDIUM),
                    selected_icon=ft.Icon(ft.Icons.LOGO_DEV, color="red", size=const.ICON_MEDIUM),
                    label="DEVELOPER MODE"
                )
            )


    def __handle_on_change(self, event):
        index = event.control.selected_index
        dest = event.control.destinations[index]

        if dest.label != "DEVELOPER MODE":
            route = f"/{dest.label.lower()}"
            self.__page.go(route)
