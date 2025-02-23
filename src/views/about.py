import flet as ft

import arrow
import platform

import app.version

class About(ft.AlertDialog):
    def __init__(self, page):
        super().__init__()

        self.__page = page
        self.__layout()


    def __layout(self):
        now = arrow.now()

        self.title = ft.Text("About")
        self.content = ft.Column(
                [
                    ft.Text(
                        f"Sixpence v{app.version.VERSION}",
                        weight=ft.FontWeight.BOLD,
                        theme_style=ft.TextThemeStyle.DISPLAY_SMALL
                    ),
                    ft.Divider(),
                    ft.Text(f"Python v{platform.python_version()} on {platform.system()} ({platform.processor()})",
                        theme_style=ft.TextThemeStyle.BODY_LARGE
                    ),
                    ft.Text(f"Flet v{ft.version.version}",
                        theme_style=ft.TextThemeStyle.BODY_LARGE
                    ),
                    ft.TextButton(
                        "View On GitHub",
                        icon=ft.Icons.LINK,
                        url="https://github.com/ccaroon/sixpence"
                    ),
                    ft.Divider(),
                    ft.Text(f"© Craig N. Caroon 2018-{now.year}",
                        theme_style=ft.TextThemeStyle.BODY_LARGE
                    ),

                ],
                width=self.__page.window.width // 2,
                height=self.__page.window.height // 2
            )


    def display(self):
        self.__page.open(self)
