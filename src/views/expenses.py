import flet as ft


class Expenses(ft.Container):
    def __init__(self, page):
        super().__init__()

        self.__page = page
        self.__layout()


    def __layout(self):
        self.content = ft.Text(
            "Expenses Placeholder",
            weight=ft.FontWeight.BOLD,
            theme_style=ft.TextThemeStyle.DISPLAY_LARGE)


    def handle_keyboard_event(self, event):
        # print(f"Expenses: KBE -> {event}")
        pass
