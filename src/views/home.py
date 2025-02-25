import flet as ft

from views.base import Base as BaseView

class Home(BaseView):
    def _layout(self):
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


        self.content = ft.Column(
            [
                header,
                ft.Divider()
            ]
        )
