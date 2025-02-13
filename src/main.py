import flet as ft
import screeninfo

def home_screen(page: ft.Page):
    icon = ft.Icon(
        name=ft.Icons.MONEY,
        size=200
        # color="red"
    )
    title = ft.Text("Sixpence", theme_style=ft.TextThemeStyle.DISPLAY_LARGE)
    stack = ft.Stack(
        [icon,title]
    )
    # header = ft.Card(
    #     # color=ft.Colors.LIGHT_GREEN_ACCENT_400,
    #     content=icon,
    #     expand=True,
    #     height=400
    # )
    # row = ft.Row([header])

    # page.add(row)
    page.add(stack)


SCREEN_SCALE_WIDTH = .70
SCREEN_SCALE_HEIGHT = .90
def main(page: ft.Page):
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
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN_900)
    page.update()

    home_screen(page)


ft.app(main)
