import flet as ft

class AppBar(ft.AppBar):
    def __init__(self, page):
        super().__init__(
            leading=ft.IconButton(ft.Icons.HOME, on_click=lambda _: page.go("/")),
            title=ft.Text("Sixpence"),
            color="black",
            bgcolor=ft.Colors.PRIMARY,
            actions=[
                ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED)
            ]
        )
