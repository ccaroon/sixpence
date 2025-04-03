import flet as ft

class NotificationBar(ft.SnackBar):
    def __init__(self, page):
        self.__page = page

        # Specific Icon and Text set elsewhere
        self.__icon = ft.Icon(color=ft.Colors.ON_SECONDARY_CONTAINER)
        self.__msg = ft.Text("", color=ft.Colors.ON_SECONDARY_CONTAINER)

        super().__init__(
            ft.Row([
                self.__icon,
                self.__msg,
            ]),
            bgcolor=ft.Colors.SECONDARY_CONTAINER
        )
        self.__page.overlay.append(self)


    def info(self, message):
        self.notify(ft.Icons.INFO_OUTLINE, message)


    def warning(self, message):
        self.notify(ft.Icons.WARNING, message)


    def error(self, message):
        self.notify(ft.Icons.ERROR, message)


    def notify(self, icon, message):
        self.__icon.name = icon
        self.__msg.value = message
        self.__page.open(self)
