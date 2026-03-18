import flet as ft

from app.sixpence import Sixpence


def main(page: ft.Page):
    _ = Sixpence(page)


ft.app(main)
