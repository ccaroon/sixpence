import flet as ft

class Router:
    def __init__(self, page, appbar, route_map):
        self.__page = page
        self.__appbar = appbar
        self.__routes = route_map

        self.__page.on_route_change = self.handle_route_change
        self.__page.on_view_pop = self.handle_view_pop

        self.__page.go("/home")


    def handle_route_change(self, event):
        self.__page.views.clear()

        self.__page.views.append(
            ft.View(
                event.route,
                [
                    # App/Nav Bar on the Left
                    ft.Row(
                        [
                            ft.Column([self.__appbar],              expand=2),
                            ft.Column([self.__routes[event.route]], expand=20)
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        expand=True
                    )
                ]
                # App/Nav Bar on Top
                # [
                #     self.__appbar,
                #     self.__routes[event.route]
                # ]
            )
        )
        self.__page.update()


    # TODO: not tested
    def handle_view_pop(self, event):
        self.__page.views.pop()
        top_view = self.__page.views[-1]
        self.__page.go(top_view.route)
