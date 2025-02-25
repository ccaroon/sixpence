import flet as ft

from views.base import Base as BaseView

class Reports(BaseView):
    def _layout(self):
        self.content = ft.Text(
            "Reports Placeholder",
            weight=ft.FontWeight.BOLD,
            theme_style=ft.TextThemeStyle.DISPLAY_LARGE)
