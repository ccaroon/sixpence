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
                    label="Home",
                    data="/home"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.FORMAT_LIST_BULLETED_OUTLINED,
                    selected_icon=ft.Icons.FORMAT_LIST_BULLETED,
                    label="Budget",
                    data="/budget"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.ATTACH_MONEY_OUTLINED,
                    selected_icon=ft.Icons.ATTACH_MONEY,
                    label="Expenses",
                    data="/expenses"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.INSERT_CHART_OUTLINED,
                    selected_icon=ft.Icons.INSERT_CHART,
                    label="Reports",
                    data="/reports"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="Settings",
                    data="/settings"
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


    def navigate_to(self, route):
        index = None
        for idx, dest in enumerate(self.destinations):
            if dest.data == route:
                index = idx
                break

        if index:
            self.selected_index = index
            self.__page.go(route)


    def __handle_on_change(self, event):
        index = event.control.selected_index
        dest = event.control.destinations[index]

        if dest.data:
            self.__page.go(dest.data)
