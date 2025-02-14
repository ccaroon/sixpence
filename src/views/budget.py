import flet as ft


class Budget(ft.Container):
    def __init__(self, page):
        super().__init__()

        self.page = page

        self.__layout()


    def __layout(self):
        self.content = ft.Text(
            "Budget Placeholder",
            color="white",
            weight=ft.FontWeight.BOLD,
            theme_style=ft.TextThemeStyle.DISPLAY_LARGE)
