import flet as ft
import screeninfo

from sixpence import Sixpence

SCREEN_SCALE_WIDTH = .70
SCREEN_SCALE_HEIGHT = .90
def main(page: ft.Page):
    # TODO: factor this mess out
    monitors = screeninfo.get_monitors()

    mon_width = monitors[0].width
    mon_height = monitors[0].height

    # TODO: reset to normal/good values
    page.window.width = mon_width * ((SCREEN_SCALE_WIDTH / 2) + (SCREEN_SCALE_WIDTH / 4))
    page.window.height = mon_height * ((SCREEN_SCALE_HEIGHT / 2) + (SCREEN_SCALE_HEIGHT / 4))
    page.window.top = mon_height * .10
    page.window.left = mon_width * .25

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # example for generating page theme colors based on the seed color
    page.theme = ft.Theme(
        font_family="Latin Modern Mono",
        color_scheme_seed=ft.Colors.GREEN_400
    )

    sixpence_app = Sixpence(page)


ft.app(main)
