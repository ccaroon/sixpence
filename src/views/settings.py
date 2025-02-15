import flet as ft


class Settings(ft.Container):
    def __init__(self, page):
        super().__init__()

        self.__page = page
        self.__layout()


    def __layout(self):
        self.content = ft.Text(
            "Settings Placeholder",
            color="white",
            weight=ft.FontWeight.BOLD,
            theme_style=ft.TextThemeStyle.DISPLAY_LARGE)
