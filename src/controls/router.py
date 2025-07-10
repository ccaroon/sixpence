import flet as ft

class Router:
    def __init__(self, page, appbar, route_map):
        self.__page = page
        self.__appbar = appbar
        self.__routes = route_map

        self.__page.on_route_change = self.__handle_route_change
        self.__page.on_view_pop = self.__handle_view_pop

        self.__active_view = self.__routes["/home"]
        self.__page.go("/home")


    def __handle_route_change(self, event):
        view = self.__routes[event.route]

        self.__page.views.clear()

        # Layout the New View
        view_contents = []

        ## Add the NavBar if exists
        if view.navbar:
            view_contents.append(view.navbar)

        ## Add the main Layout
        view_contents.append(
            ft.Row(
                [
                    ft.Column([self.__appbar], expand=2),
                    ft.Column([view],          expand=20)
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
                expand=True
            )

        )

        self.__page.views.append(
            ft.View(
                event.route,
                view_contents
            )
        )

        self.__active_view = view
        self.__page.update()


    # TODO: not tested
    def __handle_view_pop(self, event):
        if self.__page.views:
            self.__page.views.pop()

        if self.__page.views:
            top_view = self.__page.views[-1]
            self.__page.go(top_view.route)


    def handle_keyboard_event(self, event):
        """ Passes Keyboard Events to the Active View """
        # print(
        #     f"Key: {event.key}, Shift: {event.shift}, Control: {event.ctrl}, Alt: {event.alt}, Meta: {event.meta}"
        # )
        self.__active_view.handle_keyboard_event(event)
