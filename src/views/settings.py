import dateutil

import pprint

import flet as ft

from controls.notification_bar import NotificationBar
import utils.constants as const
from views.base import Base as BaseView

class Settings(BaseView):
    def __init__(self, page):
        self.__cfg = page.session.get("config")
        self.__notify_bar = NotificationBar(page)

        super().__init__(page)


    def _layout(self):
        self.content = ft.Column(
            controls=[
                # Tab View for Settings Groups
                ft.Tabs(
                    selected_index=0,
                    tabs=[
                        ft.Tab(
                            text="App",
                            icon=ft.Icons.SETTINGS_APPLICATIONS,
                            content=self.__app_controls()
                        ),
                        ft.Tab(
                            text="Backup",
                            icon=ft.Icons.BACKUP,
                            content=self.__backup_controls()
                        )
                    ]
                )
            ]
        )


    def __on_save_click(self, evt):
            self.__cfg.save()
            self.__notify_bar.info("Settings Saved")


    def __on_keep_change(self, evt):
        new_value = round(evt.control.value)
        self.__cfg.set("backup:keep", new_value)

        self.__keep_text.value = new_value
        self.__keep_text.update()


    def __on_choose_path(self, evt):
        self.__cfg.set("backup:path", evt.path)

        self.__backup_path_text.value = evt.path
        self.__backup_path_text.update()


    def __backup_controls(self):
        self.__keep_text = ft.Text(
            f"{self.__cfg.get('backup:keep')}",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
            text_align=ft.TextAlign.CENTER,
            expand=1
        )

        self.__backup_path_text = ft.Text(
            f"{self.__cfg.get('backup:path')}",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
            text_align=ft.TextAlign.CENTER,
            expand=10
        )
        file_picker = ft.FilePicker(
            on_result=self.__on_choose_path
        )
        self._page.overlay.append(file_picker)

        return ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Keep",
                                        weight=ft.FontWeight.BOLD,
                                        theme_style=ft.TextThemeStyle.TITLE_LARGE
                                    ),
                                    ft.Text(
                                        "Number of backup files to keep",
                                    ),
                                ],
                                expand=1
                            ),
                            self.__keep_text,
                            ft.Slider(
                                label="Keep {value} Backup Files",
                                min=1, max=30,
                                divisions=30,
                                value=self.__cfg.get("backup:keep"),
                                on_change_end=self.__on_keep_change,
                                expand=10
                            )
                        ]
                    ),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Path",
                                        weight=ft.FontWeight.BOLD,
                                        theme_style=ft.TextThemeStyle.TITLE_LARGE
                                    ),
                                    ft.Text(
                                        "Save backup files to this directory",
                                    ),
                                ],
                                expand=1
                            ),
                            self.__backup_path_text,
                            ft.ElevatedButton(
                                "Choose Path",
                                on_click=lambda _: file_picker.get_directory_path(),
                                expand=1
                            )
                        ]
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Save",
                                icon=ft.Icons.SAVE,
                                on_click=self.__on_save_click
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            )
        )


    def __on_mode_change(self, evt):
        new_mode = list(evt.control.selected)[0]
        self.__cfg.set("app:mode", new_mode)
        self._page.theme_mode = new_mode
        self._page.update()


    def __on_timezone_blur(self, evt):
        new_tz = evt.control.value

        if dateutil.tz.gettz(new_tz):
            self.__cfg.set("app:timezone", new_tz)
            evt.control.error_text = None
        else:
            evt.control.error_text = "Invalid Time Zone"

        evt.control.update()


    def __on_locale_blur(self, evt):
        old_locale = self.__cfg.get("app:locale")
        new_locale = evt.control.value

        if new_locale != old_locale:
            self.__cfg.set("app:locale", new_locale)
            evt.control.helper_text = "Takes affect on restart"
            evt.control.update()


    def __on_startup_view_change(self, evt):
        new_view = evt.control.value
        self.__cfg.set("app:startup_view", new_view)


    def __app_controls(self):
        return ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Mode",
                                        weight=ft.FontWeight.BOLD,
                                        theme_style=ft.TextThemeStyle.TITLE_LARGE
                                    ),
                                    ft.Text(
                                        "Light, Dark or System Default",
                                    ),
                                ],
                                expand=1
                            ),
                            ft.SegmentedButton(
                                on_change=self.__on_mode_change,
                                selected=[self.__cfg.get("app:mode")],
                                segments=[
                                    ft.Segment(
                                        value="light",
                                        label=ft.Text("Light"),
                                        icon=ft.Icon(ft.Icons.LIGHT_MODE)
                                    ),
                                    ft.Segment(
                                        value="dark",
                                        label=ft.Text("Dark"),
                                        icon=ft.Icon(ft.Icons.DARK_MODE)
                                    ),
                                    ft.Segment(
                                        value="system",
                                        label=ft.Text("System Default"),
                                        icon=ft.Icon(ft.Icons.SETTINGS_SUGGEST)
                                    )
                                ]
                            )
                        ]
                    ),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Startup View",
                                        weight=ft.FontWeight.BOLD,
                                        theme_style=ft.TextThemeStyle.TITLE_LARGE
                                    ),
                                    ft.Text(
                                        "View to open on App Startup",
                                    ),
                                ],
                                expand=1
                            ),
                            ft.Dropdown(
                                label="Startup View",
                                options=[
                                    ft.DropdownOption(key="/home", text="Home"),
                                    ft.DropdownOption(key="/budget", text="Budget"),
                                    ft.DropdownOption(key="/expenses", text="Expenses"),
                                    ft.DropdownOption(key="/reports", text="Reports"),
                                ],
                                value=self.__cfg.get("app:startup_view"),
                                on_change=self.__on_startup_view_change
                            )
                        ]
                    ),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Time Zone",
                                        weight=ft.FontWeight.BOLD,
                                        theme_style=ft.TextThemeStyle.TITLE_LARGE
                                    ),
                                    ft.Text(
                                        "IANA Defined Time Zone",
                                    ),
                                ],
                                expand=1
                            ),
                            ft.TextField(
                                label="Time Zone",
                                value=self.__cfg.get("app:timezone"),
                                on_blur=self.__on_timezone_blur
                            )
                        ]
                    ),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Locale",
                                        weight=ft.FontWeight.BOLD,
                                        theme_style=ft.TextThemeStyle.TITLE_LARGE
                                    ),
                                    ft.Text(
                                        "Language Code Identifier (en_US|es_CL|fr_FR)",
                                    ),
                                ],
                                expand=1
                            ),
                            ft.TextField(
                                label="Locale",
                                value=self.__cfg.get("app:locale"),
                                on_blur=self.__on_locale_blur
                            )
                        ]
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Save",
                                icon=ft.Icons.SAVE,
                                on_click=self.__on_save_click
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            )
        )


    def _layout_navbar(self):
        self._navbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.SETTINGS, size=const.ICON_MEDIUM),
            title=ft.Text("Settings"),
            bgcolor=ft.Colors.PRIMARY_CONTAINER
        )


    def handle_keyboard_event(self, event):
        if event.ctrl or event.meta:
            if event.key == "S":
                self.__on_save_click(None)





#
