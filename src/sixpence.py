import flet as ft

from views.home import Home
from views.budget import Budget

class Sixpence:
    def __init__(self, page):
        self.page = page

        self.__routes = {
            "/": Home(self.page),
            "/budget": Budget(self.page)
        }

        self.page.on_route_change = self.handle_route_change
        # TODO: implement to enable "Back" behavior
        # page.on_view_pop = view_pop
        self.page.go("/")

    def handle_route_change(self, event):
        # TODO: dont' do this after enable "Back" behavior????
        self.page.views.clear()

        self.page.views.append(
            ft.View(
                event.route,
                [self.__routes[event.route]]
            )
        )
        self.page.update()
