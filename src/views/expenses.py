import flet as ft

from views.base import Base as BaseView

class Expenses(BaseView):
    def _layout(self):
        self.content = ft.Text(
            "Expenses Placeholder",
            weight=ft.FontWeight.BOLD,
            theme_style=ft.TextThemeStyle.DISPLAY_LARGE)
