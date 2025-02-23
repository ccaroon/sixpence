import flet as ft


class Home(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.__page = page
        self.__layout()


    def __layout(self):
        header = ft.Container(
            ft.Row(
                [
                    ft.Column(
                        [ft.Image(src="../assets/logo.png")]
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                "Sixpence",
                                color="black",
                                weight=ft.FontWeight.BOLD,
                                theme_style=ft.TextThemeStyle.DISPLAY_LARGE),
                            ft.Text(
                                "A Simple Budget Manager",
                                color="black",
                                theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.GREEN_400
        )

        buttons1 = ft.Row(
            [
                ft.ElevatedButton(
                    "Budget",
                    color="black",
                    bgcolor="green",
                    icon=ft.Icons.FORMAT_LIST_BULLETED,
                    icon_color="black",
                    style=ft.ButtonStyle(
                        icon_size=25,
                        text_style=ft.TextStyle(
                            size=25
                        )
                    ),
                    on_click=lambda _: self.__page.go("/budget"),
                    expand=1
                ),
                ft.ElevatedButton(
                    "Expenses",
                    color="black",
                    bgcolor="red",
                    icon=ft.Icons.ATTACH_MONEY,
                    icon_color="black",
                    style=ft.ButtonStyle(
                        icon_size=25,
                        text_style=ft.TextStyle(
                            size=25
                        )
                    ),
                    expand=1
                ),
                ft.ElevatedButton(
                    "Reports",
                    color="black",
                    bgcolor="orange",
                    icon=ft.Icons.INSERT_CHART,
                    icon_color="black",
                    style=ft.ButtonStyle(
                        icon_size=25,
                        text_style=ft.TextStyle(
                            size=25
                        )
                    ),
                    expand=1
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        buttons2 = ft.Row(
            [
                ft.ElevatedButton(
                    "Settings",
                    color="black",
                    bgcolor="grey",
                    icon=ft.Icons.SETTINGS,
                    icon_color="black",
                    style=ft.ButtonStyle(
                        icon_size=25,
                        text_style=ft.TextStyle(
                            size=25
                        )
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.content = ft.Column(
            [
                header,
                ft.Divider(),
                buttons1,
                buttons2
            ]
        )

    def handle_keyboard_event(self, event):
        # print(f"Home: KBE -> {event}")
        pass
