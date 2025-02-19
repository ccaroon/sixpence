import flet as ft

from app.sixpence import Sixpence

def main(page: ft.Page):
    sixpence_app = Sixpence(page)


ft.app(main)
